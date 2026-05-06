from __future__ import annotations


def scenario_assumptions(history_growth: float = 0.05, margin: float = 0.2) -> dict[str, dict[str, float | str]]:
    return {
        "base": {"revenue_growth": history_growth, "margin_change": 0.0, "expense_ratio_change": 0.0, "description": "Historical average growth/margins/debt/working capital."},
        "optimistic": {"revenue_growth": history_growth + 0.05, "margin_change": 0.02, "expense_ratio_change": -0.02, "description": "Higher growth, better margin and collections, lower debt pressure."},
        "pessimistic": {"revenue_growth": history_growth - 0.05, "margin_change": -0.03, "expense_ratio_change": 0.03, "description": "Lower growth, higher expenses, blocked working capital, weaker OCF."},
        "stress": {"revenue_growth": -0.15, "margin_change": -0.07, "expense_ratio_change": 0.05, "description": "Revenue decline, margin compression, weak OCF, debt and liquidity pressure."},
    }
