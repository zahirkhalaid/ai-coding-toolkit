"""Risk management helpers."""

from __future__ import annotations


def position_size(equity: float, risk_per_trade: float, stop_distance: float) -> float:
    """Calculate position size given equity, risk %, and stop distance.

    Returns size such that hitting the stop loses exactly risk_per_trade of equity.
    """
    if stop_distance <= 0:
        return 0.0
    risk_amount = equity * risk_per_trade
    return risk_amount / stop_distance


def check_drawdown(equity_curve: list[float], max_allowed: float = 0.20) -> bool:
    """Return True if max drawdown exceeds max_allowed (e.g. 0.20 = 20%)."""
    if not equity_curve:
        return False
    peak = equity_curve[0]
    worst = 0.0
    for eq in equity_curve:
        if eq > peak:
            peak = eq
        dd = (peak - eq) / peak if peak > 0 else 0.0
        if dd > worst:
            worst = dd
    return worst > max_allowed