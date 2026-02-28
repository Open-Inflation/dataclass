from __future__ import annotations

import re
from typing import Literal

from pydantic import Field, field_validator

from .card import Card
from .tree import Category
from .types import NetworkModel


def _validate_hhmm(value: str, field_name: str) -> None:
    if re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
        return
    raise ValueError(f"{field_name} must match HH:MM format, got: {value!r}")


class Schedule(NetworkModel):
    """Opening/closing time in HH:MM format."""

    open_from: str | None = None
    closed_from: str | None = None

    @field_validator("open_from", "closed_from")
    @classmethod
    def validate_hhmm(cls, value: str | None, info: object) -> str | None:
        if value is None:
            return value
        field_name = getattr(info, "field_name", "time")
        _validate_hhmm(value, field_name)
        return value


class AdministrativeUnit(NetworkModel):
    """Administrative unit where the retail entity is located."""

    settlement_type: Literal["village", "city"] | None = None
    name: str | None = None
    alias: str | None = None
    country: Literal["BLR", "RUS", "USA", "ARE"] | None = None
    region: str | None = None
    longitude: float | None = None
    latitude: float | None = None


class RetailUnit(NetworkModel):
    """Retail entity: store, pickup point, or warehouse."""

    retail_type: Literal["pickup_point", "store", "warehouse"] | None = None
    code: str | None = None
    address: str | None = None
    schedule_weekdays: Schedule | None = None
    schedule_saturday: Schedule | None = None
    schedule_sunday: Schedule | None = None
    temporarily_closed: bool | None = None
    longitude: float | None = None
    latitude: float | None = None
    administrative_unit: AdministrativeUnit | None = None
    categories: list[Category] | None = Field(default_factory=list)
    products: list[Card] | None = Field(default_factory=list)
