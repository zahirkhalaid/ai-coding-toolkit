"""Backtesting engine.

Loads OHLC candle data and simulates a strategy over it, returning
equity curve, trade list, and basic performance metrics.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Candle:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass
class Trade:
    entry_time: str
    entry_price: float
    exit_time: Optional[str]
    exit_price: Optional[float]
    direction: str  # "long" or "short"
    size: float
    pnl: float = 0.0


@dataclass
class BacktestResult:
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    initial_capital: float = 10000.0

    @property
    def final_equity(self) -> float:
        return self.equity_curve[-1] if self.equity_curve else self.initial_capital

    @property
    def total_pnl(self) -> float:
        return self.final_equity - self.initial_capital

    @property
    def win_rate(self) -> float:
        if not self.trades:
            return 0.0
        wins = sum(1 for t in self.trades if (t.pnl or 0) > 0)
        return wins / len(self.trades)

    @property
    def profit_factor(self) -> float:
        gross_profit = sum(max(t.pnl or 0, 0) for t in self.trades)
        gross_loss = sum(abs(min(t.pnl or 0, 0)) for t in self.trades)
        if gross_loss == 0:
            return float("inf") if gross_profit > 0 else 0.0
        return gross_profit / gross_loss

    @property
    def max_drawdown(self) -> float:
        peak = self.initial_capital
        worst = 0.0
        for eq in self.equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak if peak > 0 else 0.0
            if dd > worst:
                worst = dd
        return worst


def load_candles(path: str | Path) -> list[Candle]:
    """Load candles from a CSV with columns: timestamp,open,high,low,close,volume."""
    candles: list[Candle] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            candles.append(
                Candle(
                    timestamp=row["timestamp"],
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", 0) or 0),
                )
            )
    return candles


def run_backtest(
    candles: list[Candle],
    signals: list[dict],
    initial_capital: float = 10000.0,
    risk_per_trade: float = 0.01,
) -> BacktestResult:
    """Run a simple backtest over a list of pre-computed signals.

    Each signal dict should have: index (int), direction ("long"/"short"),
    entry_price (float), stop_loss (float), take_profit (float).
    """
    result = BacktestResult(initial_capital=initial_capital)
    equity = initial_capital

    for sig in signals:
        idx = sig["index"]
        if idx >= len(candles):
            continue

        direction = sig["direction"]
        entry = sig["entry_price"]
        sl = sig["stop_loss"]
        tp = sig["take_profit"]

        # Size: risk_per_trade of equity on the stop distance
        stop_dist = abs(entry - sl)
        if stop_dist <= 0:
            continue
        size = (equity * risk_per_trade) / stop_dist

        # Simulate: look forward from signal index for exit
        exit_price: Optional[float] = None
        exit_time: Optional[str] = None
        pnl = 0.0

        for future in candles[idx + 1 :]:
            if direction == "long":
                if future.low <= sl:
                    exit_price = sl
                    exit_time = future.timestamp
                    pnl = (sl - entry) * size
                    break
                if future.high >= tp:
                    exit_price = tp
                    exit_time = future.timestamp
                    pnl = (tp - entry) * size
                    break
            else:  # short
                if future.high >= sl:
                    exit_price = sl
                    exit_time = future.timestamp
                    pnl = (entry - sl) * size
                    break
                if future.low <= tp:
                    exit_price = tp
                    exit_time = future.timestamp
                    pnl = (entry - tp) * size
                    break

        # If no exit hit, close at last candle close
        if exit_price is None:
            last = candles[-1]
            exit_price = last.close
            exit_time = last.timestamp
            if direction == "long":
                pnl = (exit_price - entry) * size
            else:
                pnl = (entry - exit_price) * size

        trade = Trade(
            entry_time=candles[idx].timestamp,
            entry_price=entry,
            exit_time=exit_time,
            exit_price=exit_price,
            direction=direction,
            size=size,
            pnl=pnl,
        )
        result.trades.append(trade)
        equity += pnl
        result.equity_curve.append(equity)

    return result