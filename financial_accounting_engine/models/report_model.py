from __future__ import annotations

from pydantic import BaseModel


class StakeholderSection(BaseModel):
    stakeholder: str
    priorities: list[str]
    findings: list[str]
    recommendations: list[str]
