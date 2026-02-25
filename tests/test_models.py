from __future__ import annotations

import pytest
from pydantic import ValidationError

from openinflation_dataclass import (
    AdministrativeUnit,
    Card,
    Category,
    RetailUnit,
    Schedule,
    from_json,
    to_json,
)


def _build_card() -> Card:
    return Card(
        sku="SKU-001",
        plu="123456",
        source_page_url="https://example.com/product/sku-001",
        title="Milk 1L",
        description="Pasteurized milk",
        adult=False,
        new=True,
        promo=False,
        season=False,
        hit=True,
        data_matrix=True,
        brand="Example",
        producer_name="Example Foods",
        producer_country="RUS",
        composition="Milk",
        meta_data=[],
        expiration_date_in_days=10,
        rating=4.8,
        reviews_count=124,
        price=89.9,
        discount_price=79.9,
        loyal_price=75.9,
        wholesale_price=[],
        price_unit="RUB",
        unit="PCE",
        available_count=15,
        package_quantity=1.0,
        package_unit="LTR",
        categories_uid=["milk"],
        main_image="main-image.png",
        images=["image-1.png", "image-2.png"],
    )


def _build_retail_unit() -> RetailUnit:
    category = Category(
        uid="milk",
        alias="milk",
        title="Milk",
        adult=False,
        icon="icon.png",
    )
    admin = AdministrativeUnit(
        settlement_type="city",
        name="Moscow",
        alias="moskva",
        country="RUS",
        region="Moscow",
        longitude=37.6176,
        latitude=55.7558,
    )
    return RetailUnit(
        retail_type="store",
        code="STORE-001",
        address="Example st, 1",
        schedule_weekdays=Schedule(open_from="09:00", closed_from="22:00"),
        schedule_saturday=Schedule(open_from="09:00", closed_from="22:00"),
        schedule_sunday=Schedule(open_from="10:00", closed_from="21:00"),
        temporarily_closed=False,
        longitude=37.6176,
        latitude=55.7558,
        administrative_unit=admin,
        categories=[category],
        products=[_build_card()],
    )


def test_round_trip_retail_unit_json() -> None:
    retail = _build_retail_unit()
    payload = to_json(retail)
    restored = from_json(payload, RetailUnit)

    assert isinstance(restored, RetailUnit)
    assert restored.products[0].sku == "SKU-001"
    assert restored.products[0].main_image == "main-image.png"
    assert restored.categories[0].icon is not None
    assert restored.categories[0].icon == "icon.png"


def test_round_trip_list_of_cards_json() -> None:
    payload = to_json([_build_card()])
    restored = from_json(payload, list[Card])

    assert isinstance(restored, list)
    assert isinstance(restored[0], Card)
    assert restored[0].images[1] == "image-2.png"


def test_card_piece_validation_rejects_float_count() -> None:
    with pytest.raises(ValidationError):
        Card(
            sku="SKU-001",
            plu="123456",
            source_page_url="https://example.com/product/sku-001",
            title="Milk 1L",
            description="Pasteurized milk",
            adult=False,
            new=True,
            promo=False,
            season=False,
            hit=True,
            data_matrix=True,
            brand="Example",
            producer_name="Example Foods",
            producer_country="RUS",
            composition="Milk",
            meta_data=[],
            expiration_date_in_days=10,
            rating=4.8,
            reviews_count=124,
            price=89.9,
            discount_price=79.9,
            loyal_price=75.9,
            wholesale_price=[],
            price_unit="RUB",
            unit="PCE",
            available_count=15.5,
            package_quantity=1.0,
            package_unit="LTR",
            categories_uid=["milk"],
            main_image="main-image.png",
        )


def test_schedule_validation_rejects_invalid_time_format() -> None:
    with pytest.raises(ValidationError):
        Schedule(open_from="9:00", closed_from="21:00")
