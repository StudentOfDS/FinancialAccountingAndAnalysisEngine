from __future__ import annotations

from pydantic import BaseModel


class ForecastPoint(BaseModel):
    metric: str
    period: str
    expected: float
    lower: float
    upper: float
    model: str
    accuracy: dict[str, float | None]
    explanation: str
