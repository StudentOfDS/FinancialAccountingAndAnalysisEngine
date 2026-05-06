from __future__ import annotations

from typing import Any


def export_html(report: dict[str, Any]) -> str:
    parts = ["<html><body><h1>Financial Intelligence Stakeholder Report</h1>"]
    health = report.get("health", {})
    sections = report.get("sections", {})
    parts.append(f"<h2>Health</h2><p>{health.get('explanation', '')}</p>")
    parts.append("<h2>Stakeholders</h2>")
    for stakeholder, findings in sections.items():
        parts.append(
            f"<h3>{stakeholder.title()}</h3><ul>"
            + "".join(f"<li>{item}</li>" for item in findings)
            + "</ul>"
        )
    parts.append("</body></html>")
    return "".join(parts)
