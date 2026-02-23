from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .tree import Category
    from .card import Card

class Schedule:
    """Время формата HH:MM"""
    open_from: str
    closed_from: str

class AdministrativeUnit:
    settlement_type: Literal["village", "city"]

    name: str
    country: Literal["BLR", "RUS", "USA", "ARE"]
    region: str

    longitude: float
    latitude: float

class RetailUnit:
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

    categories: list[Category]
    products: list[Card]

