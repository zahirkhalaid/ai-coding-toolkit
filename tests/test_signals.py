"""Tests for signal detectors."""

from ai_coding_toolkit.backtest import Candle
from ai_coding_toolkit.signals import detect_fvg, detect_order_block, detect_liquidity_sweep


def _bullish_fvg_candles() -> list[Candle]:
    # t0 high=100, t2 low=101 -> bullish FVG gap up
    return [
        Candle("t0", 98.0, 100.0, 97.0, 99.0),
        Candle("t1", 99.0, 100.5, 98.5, 100.0),
        Candle("t2", 100.0, 102.0, 101.0, 101.5),
        Candle("t3", 101.5, 103.0, 101.0, 102.5),
    ]


def test_fvg_bullish():
    candles = _bullish_fvg_candles()
    signals = detect_fvg(candles)
    assert len(signals) >= 1
    assert signals[0]["direction"] == "long"
    assert signals[0]["type"] == "fvg_bullish"


def test_detectors_return_dicts():
    candles = _bullish_fvg_candles()
    for detector in (detect_fvg, detect_order_block, detect_liquidity_sweep):
        sigs = detector(candles)
        for s in sigs:
            assert "index" in s
            assert "direction" in s
            assert s["direction"] in ("long", "short")
            assert "entry_price" in s
            assert "stop_loss" in s
            assert "take_profit" in s
            assert "type" in s