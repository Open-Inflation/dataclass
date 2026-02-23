from __future__ import annotations

from pydantic import Field

from .types import Base64BytesIO, NetworkModel


class Category(NetworkModel):
    """Категория товаров с иерархией вложенности."""

    uid: str
    alias: str
    title: str
    adult: bool

    icon: Base64BytesIO | None = Field(default=None, repr=False)
    banner: Base64BytesIO | None = Field(default=None, repr=False)
    children: list[Category] = Field(default_factory=list)


Category.model_rebuild()
