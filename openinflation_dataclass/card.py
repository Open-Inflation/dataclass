from typing import Literal, TypedDict
from io import BytesIO


class WholesalePrice(TypedDict):
    from_items: float | int
    """От какого кол-ва товаров начинает применяться скидка (включительно)"""
    price: float
    """Цена за единицу товара"""

class Card:
    sku: str
    """Уникальный внутренний код товара в системе учета компании."""
    plu: str | None
    """Код для быстрого поиска цены на кассе."""
    source_page_url: str
    """Ссылка на исходную страницу"""

    title: str
    """Название товара"""

    abult: bool
    """Помечен ли товар как 18+"""
    new: bool
    """Отмечает ли магазин товар как новый"""
    promo: bool
    """Отмечает ли магазин товар промо акцией"""
    season: bool
    """Является ли товар сезонным"""
    hit: bool
    """Отмечает ли магазин товар как хит"""
    data_matrix: bool
    """Использует ли выбранный товар QR-код для пробива на кассе"""

    brand_uid: str

    price: float
    """Регулярная цена"""
    discount_price: float | None
    """Скидочная цена"""
    loyal_price: float | None
    """Скидка по карте лояльности"""
    wholesale_price: list[WholesalePrice]
    """Оптовая цена"""

    price_unit: Literal["BYN", "RUB", "USD", "EUR", "AED"]
    """Валюта цены"""

    unit: Literal["PCE", "KGM", "LTR"]
    """Единицы измерения товара по стандарту UNECE Rec 20"""
    available_count: float | int
    """Доступное кол-во товара в магазине (для PCE допускается лишь int)"""

    categories_uid: list[str]
    """Список категорий которому соответсвует товар"""

    main_image: BytesIO
    """Главное изображение товара"""
    images: list[BytesIO]
    """Остальные изображения товара (без главного)"""

# TODO brand class
