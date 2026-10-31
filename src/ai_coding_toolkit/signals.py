"""Signal detectors: FVG, order block, liquidity sweep.

These are simple, illustrative ICT-style detectors. They return lists of
signal dicts that can be fed directly into run_backtest().
"""

from __future__ import annotations

from typing import Optional

from .backtest import Candle


def detect_fvg(candles: list[Candle], lookback: int = 3) -> list[dict]:
    """Detect Fair Value Gaps (FVG).

    A bullish FVG: candle[i-1].high < candle[i+1].low (gap up).
    A bearish FVG: candle[i-1].low > candle[i+1].high (gap down).
    Returns signal dicts at the index of the middle candle.
    """
    signals: list[dict] = []
    for i in range(1, len(candles) - 1):
        prev = candles[i - 1]
        curr = candles[i]
        nxt = candles[i + 1]

        # Bullish FVG: gap up between prev high and next low
        if prev.high < nxt.low:
            signals.append(
                {
                    "index": i,
                    "direction": "long",
                    "entry_price": curr.close,
                    "stop_loss": min(prev.low, curr.low),
                    "take_profit": nxt.high,
                    "type": "fvg_bullish",
                }
            )
        # Bearish FVG: gap down between prev low and next high
        elif prev.low > nxt.high:
            signals.append(
                {
                    "index": i,
                    "direction": "short",
                    "entry_price": curr.close,
                    "stop_loss": max(prev.high, curr.high),
                    "take_profit": nxt.low,
                    "type": "fvg_bearish",
                }
            )
    return signals


def detect_order_block(candles: list[Candle], lookback: int = 5) -> list[dict]:
    """Detect simple order blocks: last opposite candle before a strong move.

    A bullish OB: last bearish candle before a strong bullish candle.
    A bearish OB: last bullish candle before a strong bearish candle.
    """
    signals: list[dict] = []
    for i in range(lookback, len(candles)):
        curr = candles[i]
        # Strong move: body > 2x average body of lookback
        avg_body = sum(
            abs(candles[j].close - candles[j].open) for j in range(i - lookback, i)
        ) / lookback
        curr_body = abs(curr.close - curr.open)

        if curr_body <= 2 * avg_body:
            continue

        # Find last opposite-colored candle before this move
        for j in range(i - 1, max(i - lookback - 1, 0), -1):
            prev = candles[j]
            if curr.close > curr.open and prev.close < prev.open:
                # Bullish move after bearish candle = bullish OB
                signals.append(
                    {
                        "index": j,
                        "direction": "long",
                        "entry_price": (prev.open + prev.close) / 2,
                        "stop_loss": min(prev.low, curr.low),
                        "take_profit": curr.high,
                        "type": "ob_bullish",
                    }
                )
                break
            elif curr.close < curr.open and prev.close > prev.open:
                # Bearish move after bullish candle = bearish OB
                signals.append(
                    {
                        "index": j,
                        "direction": "short",
                        "entry_price": (prev.open + prev.close) / 2,
                        "stop_loss": max(prev.high, curr.high),
                        "take_profit": curr.low,
                        "type": "ob_bearish",
                    }
                )
                break
    return signals


def detect_liquidity_sweep(candles: list[Candle], lookback: int = 10) -> list[dict]:
    """Detect liquidity sweeps: price breaks a recent high/low then reverses.

    Bullish sweep: price makes new low, then closes above prior low.
    Bearish sweep: price makes new high, then closes below prior high.
    """
    signals: list[dict] = []
    for i in range(lookback, len(candles)):
        window = candles[i - lookback : i]
        curr = candles[i]

        recent_low = min(c.low for c in window)
        recent_high = max(c.high for c in window)

        # Bullish sweep: swept below recent low, then reclaimed
        if curr.low < recent_low and curr.close > recent_low:
            signals.append(
                {
                    "index": i,
                    "direction": "long",
                    "entry_price": curr.close,
                    "stop_loss": curr.low,
                    "take_profit": recent_high,
                    "type": "sweep_bullish",
                }
            )
        # Bearish sweep: swept above recent high, then rejected
        elif curr.high > recent_high and curr.close < recent_high:
            signals.append(
                {
                    "index": i,
                    "direction": "short",
                    "entry_price": curr.close,
                    "stop_loss": curr.high,
                    "take_profit": recent_low,
                    "type": "sweep_bearish",
                }
            )
    return signals