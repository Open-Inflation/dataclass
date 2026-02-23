# openinflation-dataclass

Typed `pydantic` models for:
- product cards (`Card`);
- category trees (`Category`);
- geolocation and retail entities (`AdministrativeUnit`, `RetailUnit`, `Schedule`).

The package also includes network serialization helpers:
- `to_json(value)` to convert model data to transport JSON;
- `from_json(payload, model)` to restore typed objects from JSON.

## Installation

```bash
pip install openinflation-dataclass
```

## Quick Start

```python
from io import BytesIO

from openinflation_dataclass import (
    AdministrativeUnit,
    Card,
    Category,
    RetailUnit,
    Schedule,
    from_json,
    to_json,
)

category = Category(uid="milk", alias="milk", title="Milk", adult=False)

card = Card(
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
    categories_uid=[category.uid],
    main_image=BytesIO(b"main-image"),
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

retail = RetailUnit(
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
    products=[card],
)

payload = to_json(retail)
restored = from_json(payload, RetailUnit)
```

`BytesIO` fields are encoded as base64 strings in JSON and restored back to `BytesIO` on `from_json`.

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
pytest
python -m build
twine check dist/*
```

## Publishing to PyPI via Trusted Publisher

The repository contains `.github/workflows/publish.yml` that publishes via OIDC (no API token).
Optional dry-run publishing is available in `.github/workflows/publish-testpypi.yml`.

1. Create a `pypi` environment in GitHub repository settings.
2. On PyPI, add a Trusted Publisher for this repository with:
   - Owner: `Open-Inflation`
   - Repository: `dataclass`
   - Workflow: `publish.yml`
   - Environment: `pypi`
3. Create a GitHub Release (or run `workflow_dispatch`) to publish.
4. (Optional) Configure a second Trusted Publisher in TestPyPI for `publish-testpypi.yml`
   and environment `testpypi`, then run that workflow for pre-release validation.
