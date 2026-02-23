from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .types import Base64BytesIO, NetworkModel


class WholesalePrice(NetworkModel):
    """Цена за единицу при оптовом пороге."""

    from_items: int | float
    price: float


class MetaData(NetworkModel):
    """Дополнительные метаданные товара."""

    name: str
    alias: str
    value: float | int | str


class Card(NetworkModel):
    """Карточка товара из источника."""

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

    # Гайд на единицы:
    # Шоколад 200г:
    #   unit="PCE", available_count=15, package_quantity=0.2, package_unit="KGM"
    # Молоко 1л:
    #   unit="PCE", available_count=10, package_quantity=1, package_unit="LTR"
    # Картошка на развес:
    #   unit="KGM", available_count=12.7, package_quantity=None, package_unit=None
    # Водомат:
    #   unit="LTR", available_count=29.2, package_quantity=0.5, package_unit="LTR"
    unit: Literal["PCE", "KGM", "LTR"]
    available_count: int | float | None
    package_quantity: float | None
    package_unit: Literal["KGM", "LTR"] | None

    categories_uid: list[str]

    main_image: Base64BytesIO = Field(repr=False)
    images: list[Base64BytesIO] = Field(default_factory=list, repr=False)

    @model_validator(mode="after")
    def validate_business_rules(self) -> Card:
        if self.unit == "PCE" and self.available_count is not None and type(self.available_count) is not int:
            raise ValueError("Для unit='PCE' поле available_count должно быть int.")
        if (self.package_quantity is None) != (self.package_unit is None):
            raise ValueError("package_quantity и package_unit должны быть заполнены вместе или оба быть None.")
        return self
