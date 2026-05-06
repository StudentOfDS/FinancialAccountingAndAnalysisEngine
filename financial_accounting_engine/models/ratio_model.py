from __future__ import annotations

from pydantic import BaseModel


class RatioResult(BaseModel):
    period: str | None = None
    ratio_name: str
    value: float | None
    interpretation: str
    warning: str | None = None
