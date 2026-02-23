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
    raise ValueError(f"{field_name} должно быть во времени формата HH:MM, получено: {value!r}")


class Schedule(NetworkModel):
    """Время открытия/закрытия в формате HH:MM."""

    open_from: str
    closed_from: str

    @field_validator("open_from", "closed_from")
    @classmethod
    def validate_hhmm(cls, value: str, info: object) -> str:
        field_name = getattr(info, "field_name", "time")
        _validate_hhmm(value, field_name)
        return value


class AdministrativeUnit(NetworkModel):
    """Административная единица, в рамках которой расположен объект."""

    settlement_type: Literal["village", "city"]
    name: str
    alias: str
    country: Literal["BLR", "RUS", "USA", "ARE"]
    region: str
    longitude: float
    latitude: float


class RetailUnit(NetworkModel):
    """Торговая точка: магазин, ПВЗ или склад."""

    retail_type: Literal["pickup_point", "store", "warehouse"]
    code: str
    address: str
    schedule_weekdays: Schedule
    schedule_saturday: Schedule
    schedule_sunday: Schedule
    temporarily_closed: bool
    longitude: float
    latitude: float
    administrative_unit: AdministrativeUnit
    categories: list[Category] = Field(default_factory=list)
    products: list[Card] = Field(default_factory=list)
