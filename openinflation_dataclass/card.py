from typing import Literal, TypedDict
from io import BytesIO


class WholesalePrice(TypedDict):
    from_items: float | int
    """От какого кол-ва товаров начинает применяться скидка (включительно)"""
    price: float
    """Цена за единицу товара"""

class MetaData(TypedDict):
    name: str
    """Человеко-читаемое название поля"""
    alias: str
    """Уникальный alias (английский в нижнем регистре, цифры допустимы)"""
    value: float | int | str
    """Значение"""

class Card:
    sku: str
    """Уникальный внутренний код товара в системе учета компании."""
    plu: str | None
    """Код для быстрого поиска цены на кассе."""
    source_page_url: str
    """Ссылка на исходную страницу"""

    title: str
    """Название товара"""
    description: str
    """Описание товара"""

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

    brand: str
    """Бренд товара"""
    producer_name: str
    """Название производителя"""
    producer_country: Literal["BLR", "RUS", "USA", "ARE"]
    """Страна-производитель"""

    composition: str
    """Состав"""

    meta_data: list[MetaData]
    """Любые метаданные (например пищевая ценность или габариты)"""

    expiration_date_in_days: int
    """Срок годности с момента производства в днях"""

    rating: float
    """Пятибальная шкала с детализацией до десятых"""
    reviews_count: int
    """Кол-во отзывов по заявлению источника"""

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

    ### ГАЙД НА ЕДИНИЦЫ
    # Шоколад 200г:
    #     unit=PCE
    #     available_count=15
    #     package_quantity=0.2
    #     package_unit=KGM
    # Молоко 1л:
    #     unit=PCE
    #     available_count=10
    #     package_quantity=1
    #     package_unit=LTR
    # Картошка (на развес):
    #     unit=KGM
    #     available_count=12.7
    #     package_quantity=None
    #     package_unit=None
    # Водомат:
    #     unit=LTR
    #     available_count=29.2
    #     package_quantity=LTR
    # потому что выдает с фиксированным шагом (указываем самый мелкий)
    #     package_unit=0.5

    unit: Literal["PCE", "KGM", "LTR"]
    """Единицы измерения товара по стандарту UNECE Rec 20"""
    available_count: float | int
    """Доступное кол-во товара в магазине (для PCE допускается лишь int)"""
    package_quantity: float | None
    """Объем/вес товара в упаковке"""
    package_unit: Literal["KGM", "LTR"] | None
    """Единица измерения кпаковки"""

    categories_uid: list[str]
    """Список категорий которому соответсвует товар"""

    main_image: BytesIO
    """Главное изображение товара"""
    images: list[BytesIO]
    """Остальные изображения товара (без главного)"""

# TODO brand class
