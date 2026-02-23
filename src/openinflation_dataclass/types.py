from __future__ import annotations

import base64
import binascii
from io import BytesIO
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ConfigDict, PlainSerializer


def _bytesio_from_network(value: Any) -> BytesIO:
    if isinstance(value, BytesIO):
        return value
    if isinstance(value, (bytes, bytearray)):
        return BytesIO(bytes(value))
    if isinstance(value, str):
        try:
            raw = base64.b64decode(value.encode("ascii"), validate=True)
        except (ValueError, UnicodeEncodeError, binascii.Error) as exc:
            raise ValueError("Некорректная base64-строка для BytesIO.") from exc
        return BytesIO(raw)
    raise TypeError(f"Ожидался BytesIO/base64-строка/bytes, получено: {type(value)!r}")


def _bytesio_to_network(value: BytesIO) -> str:
    return base64.b64encode(value.getvalue()).decode("ascii")


Base64BytesIO = Annotated[
    BytesIO,
    BeforeValidator(_bytesio_from_network),
    PlainSerializer(_bytesio_to_network, return_type=str, when_used="json"),
]


class NetworkModel(BaseModel):
    """Базовая pydantic-модель для сетевых сущностей."""

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )
