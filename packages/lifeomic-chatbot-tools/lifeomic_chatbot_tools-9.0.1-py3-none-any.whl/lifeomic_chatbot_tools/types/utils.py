import hashlib
import json

from pydantic.v1 import BaseModel


def hash_model(obj: BaseModel, **kwargs) -> str:
    """
    Creates a deterministic hash of ``obj``, which is some pydantic model. All keyword arguments are forwarded on to
    :meth:`pydantic.BaseModel.json`.
    """
    data = obj.json(**kwargs)
    raw = json.dumps(data, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    return digest
