from __future__ import annotations

import json
from typing import Any, TypeVar

from pydantic import TypeAdapter

T = TypeVar("T")


def to_json(value: Any, *, ensure_ascii: bool = False) -> str:
    """Serialize pydantic models/structures to a JSON string."""
    normalized = TypeAdapter(Any).dump_python(value, mode="json")
    return json.dumps(normalized, ensure_ascii=ensure_ascii, separators=(",", ":"))


def from_json(payload: str | bytes | bytearray, model: type[T] | Any) -> T:
    """Deserialize a JSON payload into a target pydantic type."""
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")
    raw = json.loads(payload)
    return TypeAdapter(model).validate_python(raw)
