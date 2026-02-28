from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .types import NetworkModel


class WholesalePrice(NetworkModel):
    """Wholesale unit price threshold."""

    from_items: int | float | None = None
    price: float | None = None


class MetaData(NetworkModel):
    """Additional product metadata."""

    name: str | None = None
    alias: str | None = None
    value: float | int | str | None = None


class Card(NetworkModel):
    """Product card model from a source catalog."""

    sku: str | None = None
    plu: str | None = None
    source_page_url: str | None = None

    title: str | None = None
    description: str | None = None

    adult: bool | None = None
    new: bool | None = None
    promo: bool | None = None
    season: bool | None = None
    hit: bool | None = None
    data_matrix: bool | None = None

    brand: str | None = None
    producer_name: str | None = None
    producer_country: Literal["BLR", "RUS", "USA", "ARE", "CHN"] | None = None

    composition: str | None = None
    meta_data: list[MetaData] | None = Field(default_factory=list)

    expiration_date_in_days: int | None = None

    rating: float | None = None
    reviews_count: int | None = None

    price: float | None = None
    discount_price: float | None = None
    loyal_price: float | None = None
    wholesale_price: list[WholesalePrice] | None = Field(default_factory=list)
    price_unit: Literal["BYN", "RUB", "USD", "EUR", "AED"] | None = None

    # Unit guide:
    # Chocolate 200 g:
    #   unit="PCE", available_count=15, package_quantity=0.2, package_unit="KGM"
    # Milk 1 L:
    #   unit="PCE", available_count=10, package_quantity=1, package_unit="LTR"
    # Potatoes by weight:
    #   unit="KGM", available_count=12.7, package_quantity=None, package_unit=None
    # Water vending:
    #   unit="LTR", available_count=29.2, package_quantity=0.5, package_unit="LTR"
    unit: Literal["PCE", "KGM", "LTR"] | None = None
    available_count: int | float | None = None
    package_quantity: float | None = None
    package_unit: Literal["KGM", "LTR"] | None = None

    categories_uid: list[str] | None = Field(default_factory=list)

    main_image: str | None = Field(default=None, repr=False)
    images: list[str] | None = Field(default_factory=list, repr=False)

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
