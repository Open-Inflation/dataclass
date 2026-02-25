from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class NetworkModel(BaseModel):
    """Base pydantic model for network-facing entities."""

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )
