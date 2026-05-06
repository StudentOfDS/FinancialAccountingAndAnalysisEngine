from __future__ import annotations

from typing import Any


def export_pdf_text(report: dict[str, Any]) -> bytes:
    health = report.get("health", {})
    text = "Financial Intelligence Stakeholder Report\n" + str(health.get("explanation", ""))
    return text.encode("utf-8")
