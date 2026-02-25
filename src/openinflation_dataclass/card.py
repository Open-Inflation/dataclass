from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .types import NetworkModel


class WholesalePrice(NetworkModel):
    """Wholesale unit price threshold."""

    from_items: int | float
    price: float


class MetaData(NetworkModel):
    """Additional product metadata."""

    name: str
    alias: str
    value: float | int | str


class Card(NetworkModel):
    """Product card model from a source catalog."""

    sku: str
    plu: str | None
    source_page_url: str

    title: str
    description: str

    adult: bool
    new: bool
    promo: bool
    season: bool
    hit: bool
    data_matrix: bool

    brand: str
    producer_name: str
    producer_country: Literal["BLR", "RUS", "USA", "ARE", "CHN"]

    composition: str
    meta_data: list[MetaData]

    expiration_date_in_days: int

    rating: float
    reviews_count: int

    price: float
    discount_price: float | None
    loyal_price: float | None
    wholesale_price: list[WholesalePrice]
    price_unit: Literal["BYN", "RUB", "USD", "EUR", "AED"]

    # Unit guide:
    # Chocolate 200 g:
    #   unit="PCE", available_count=15, package_quantity=0.2, package_unit="KGM"
    # Milk 1 L:
    #   unit="PCE", available_count=10, package_quantity=1, package_unit="LTR"
    # Potatoes by weight:
    #   unit="KGM", available_count=12.7, package_quantity=None, package_unit=None
    # Water vending:
    #   unit="LTR", available_count=29.2, package_quantity=0.5, package_unit="LTR"
    unit: Literal["PCE", "KGM", "LTR"]
    available_count: int | float | None
    package_quantity: float | None
    package_unit: Literal["KGM", "LTR"] | None

    categories_uid: list[str]

    main_image: str = Field(repr=False)
    images: list[str] = Field(default_factory=list, repr=False)

    @model_validator(mode="after")
    def validate_business_rules(self) -> Card:
        is_piece_unit = self.unit == "PCE"
        has_count = self.available_count is not None
        count_is_int = type(self.available_count) is int

        if is_piece_unit and has_count and not count_is_int:
            raise ValueError("For unit='PCE', available_count must be int.")
        if (self.package_quantity is None) != (self.package_unit is None):
            raise ValueError(
                "package_quantity and package_unit must be set together or both set to None."
            )
        return self
