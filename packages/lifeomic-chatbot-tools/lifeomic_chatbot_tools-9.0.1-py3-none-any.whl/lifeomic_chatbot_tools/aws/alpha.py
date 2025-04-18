import asyncio
import json
import logging
import typing as t
from json import JSONDecodeError
from logging import Logger

from httpx import AsyncClient
from pydantic.v1 import BaseModel, ValidationError
from tenacity import RetryCallState

from lifeomic_chatbot_tools._utils import ImportExtraError
from lifeomic_chatbot_tools.utils import coalesce


try:
    import boto3
    from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential_jitter
except ImportError:
    raise ImportExtraError("aws", __name__)

HttpMethod = t.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class _AsyncLambdaClient:
    def __init__(self):
        self.__client: t.Any = None

    @property
    def _client(self):
        """Lazily instantiated boto3 Lambda client."""
        if not self.__client:
            self.__client = boto3.client("lambda")
        return self.__client

    async def invoke(self, FunctionName: str, Payload: str):
        """
        A wrapper around boto3's Lambda `invoke` method that makes the call asynchronous, enabling parallel Lambda
        invocations to be made in Python code. The Lambda is still invoked synchronously, but the Python code can
        continue to run other tasks while waiting for the Lambda to complete.
        """
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, lambda: self._client.invoke(FunctionName=FunctionName, Payload=Payload))
        return res


class AlphaResponse(BaseModel):
    status_code: int
    """The http response status code."""
    text: str
    """The http response body."""
    url: str
    """The full URL that was called to generate this response."""
    method: HttpMethod
    """The HTTP request's method."""

    @property
    def body(self):
        """Attempts to parse the response body as JSON."""
        try:
            return json.loads(self.text)
        except JSONDecodeError as e:
            raise RuntimeError(f"could not parse text {self.text} as json, reason: {e}")

    @property
    def ok(self):
        """Returns ``True`` if the response's status code is in the 200-300 range."""
        return self.status_code < 400

    def raise_for_status(self):
        """Raises an exception if the response status code is not in the 200-300 range."""
        if not self.ok:
            raise AssertionError(
                f"Found not ok status {self.status_code} from request "
                f"{self.method} {self.url}. Response body: {self.text}"
            )


def is_retryable_error(res: AlphaResponse):
    return res.status_code == 429 or (500 <= res.status_code < 600)


class AlphaConfig(t.TypedDict, total=False):
    params: dict[str, t.Any]
    """Request query parameters."""
    headers: dict[str, str]
    """Request headers."""
    attempts: int
    """Maximum number of attempts to make for a request."""
    retry_condition: t.Callable[[AlphaResponse], bool]
    """
    If function returns ``True``, the request will be retried. The function accepts the
    most recent response as the argument.
    """
    retry_initial_wait: int
    """Number of seconds to wait before the first retry."""
    retry_max_wait: int
    """Maximum number of seconds to wait between retries."""
    logger: Logger


DEFAULT_ATTEMPTS = 3
DEFAULT_RETRY_CONDITION = is_retryable_error
DEFAULT_RETRY_INITIAL_WAIT = 1
DEFAULT_RETRY_MAX_WAIT = 10
DEFAULT_LOGGER = logging.getLogger(__name__)


class Alpha:
    """
    A minimal Python port of LifeOmic's `alpha` utility for calling Lambda functions that operate
    as web services using the [AWS API Gateway event format](https://docs.aws.amazon.com/lambda/latest/dg/services-apiga
    teway.html#apigateway-example-event).
    """

    def __init__(self, target: str, **cfg: t.Unpack[AlphaConfig]):
        """
        If ``target`` begins with ``lambda://`` e.g. ``lambda://function-name``, then ``boto3`` will attempt to use the
        environment credentials and call an actual Lambda function named ``function-name``. Alternatively, an actual URL
        can be passed in as the ``target`` to support calling e.g. a locally running Lambda function.
        """
        self._cfg = cfg
        self._target = target
        self._lambda_client: t.Optional[_AsyncLambdaClient] = None
        self._http_client: t.Optional[AsyncClient] = None
        prefix = "lambda://"
        if target.startswith(prefix):
            self._target = target[len(prefix) :]
            self._lambda_client = _AsyncLambdaClient()
        else:
            self._http_client = AsyncClient()

    def get(self, path: str, **cfg: t.Unpack[AlphaConfig]):
        return self.request(path=path, method="GET", **cfg)

    def post(self, path: str, body: t.Any = None, **cfg: t.Unpack[AlphaConfig]):
        return self.request(path=path, method="POST", body=body, **cfg)

    def put(self, path: str, body: t.Any = None, **cfg: t.Unpack[AlphaConfig]):
        return self.request(path=path, method="PUT", body=body, **cfg)

    def patch(self, path: str, body: t.Any = None, **cfg: t.Unpack[AlphaConfig]):
        return self.request(path=path, method="PATCH", body=body, **cfg)

    def delete(self, path: str, **cfg: t.Unpack[AlphaConfig]):
        return self.request(path=path, method="DELETE", **cfg)

    def request(
        self,
        *,
        path: str,
        method: HttpMethod,
        body: t.Any = None,
        **cfg: t.Unpack[AlphaConfig],
    ):
        payload: t.Dict[str, t.Union[str, t.Dict[str, str]]] = {"path": path, "httpMethod": method}
        if body:
            payload["body"] = json.dumps(body)
        params = {**self._cfg.get("params", {}), **cfg.get("params", {})}
        if params:
            payload["queryStringParameters"] = params
        all_headers = {**self._cfg.get("headers", {}), **cfg.get("headers", {})}
        if all_headers:
            payload["headers"] = all_headers

        attempts = coalesce((self._cfg.get("attempts"), cfg.get("attempts")), DEFAULT_ATTEMPTS)
        retry_initial_wait = coalesce(
            (self._cfg.get("retry_initial_wait"), cfg.get("retry_initial_wait")), DEFAULT_RETRY_INITIAL_WAIT
        )
        retry_max_wait = coalesce((self._cfg.get("retry_max_wait"), cfg.get("retry_max_wait")), DEFAULT_RETRY_MAX_WAIT)
        retry_condition = coalesce(
            (self._cfg.get("retry_condition"), cfg.get("retry_condition")), DEFAULT_RETRY_CONDITION
        )

        def log_attempt(state: RetryCallState):
            logger = coalesce([self._cfg.get("logger"), cfg.get("logger")], DEFAULT_LOGGER)
            res = t.cast(AlphaResponse, state.outcome.result()) if state.outcome else None
            logger_data = (
                {"httpMethod": res.method, "statusCode": res.status_code, "requestUrl": res.url} if res else {}
            )
            logger.warning({"msg": "Request failed. Retrying.", "attempt": state.attempt_number, **logger_data})

        invoke_lambda_with_retry = retry(
            retry=retry_if_result(retry_condition),
            stop=stop_after_attempt(attempts),
            wait=wait_exponential_jitter(initial=retry_initial_wait, max=retry_max_wait),
            # If all retries are exhausted, return the result of the final attempt.
            retry_error_callback=lambda state: state.outcome.result() if state.outcome else None,
            before_sleep=log_attempt,
        )(self._invoke_lambda)
        return invoke_lambda_with_retry(payload)

    async def _invoke_lambda(self, payload: dict):
        if self._lambda_client:
            res = await self._lambda_client.invoke(FunctionName=self._target, Payload=json.dumps(payload))
            if res.get("FunctionError"):
                # This was an unhandled function error. Return 502 just like API Gateway would.
                # Source: https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-errors.html
                res_payload = json.dumps(
                    {"statusCode": 502, "body": json.dumps({"message": "Internal server error"})}
                ).encode("utf-8")
            else:
                res_payload = t.cast(bytes, res["Payload"].read())
        else:
            assert self._http_client  # this should never fail but we put it here to satisfy the typing engine
            res = await self._http_client.post(self._target, json=payload)
            res_payload = res.content
        return self._parse_response(
            payload=res_payload, url=self._target + payload["path"], method=payload["httpMethod"]
        )

    @staticmethod
    def _parse_response(*, payload: bytes, url: str, method: HttpMethod):
        """Creates an `AlphaResponse` object from a raw Lambda response payload."""
        try:
            parsed = json.loads(payload.decode("utf-8"))
            return AlphaResponse(status_code=parsed["statusCode"], text=parsed["body"], url=url, method=method)
        except (JSONDecodeError, KeyError, ValidationError) as e:
            raise RuntimeError(f"could not parse payload {payload!r} as an API Gateway event, reason: {e}")
