from __future__ import annotations

from pydantic import BaseModel


class ChartSpec(BaseModel):
    chart_id: str
    title: str
    business_question: str
    chart_type: str
