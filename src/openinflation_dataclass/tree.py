from __future__ import annotations

from pydantic import Field

from .types import NetworkModel


class Category(NetworkModel):
    """Product category with nested children."""

    uid: str
    alias: str
    title: str
    adult: bool

    icon: str | None = Field(default=None, repr=False)
    banner: str | None = Field(default=None, repr=False)
    children: list[Category] = Field(default_factory=list)


Category.model_rebuild()
