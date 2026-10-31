"""Tests for the backtesting engine."""

from ai_coding_toolkit.backtest import Candle, run_backtest
from ai_coding_toolkit.signals import detect_fvg


def _make_candles() -> list[Candle]:
    return [
        Candle("t0", 100.0, 102.0, 99.0, 101.0),
        Candle("t1", 101.0, 103.0, 100.0, 102.0),
        Candle("t2", 102.0, 104.0, 101.0, 103.0),  # bullish FVG vs t0/t3
        Candle("t3", 103.0, 105.0, 103.5, 104.0),  # next low > prev high
        Candle("t4", 104.0, 105.0, 103.0, 104.5),
    ]


def test_load_and_backtest_runs():
    candles = _make_candles()
    signals = detect_fvg(candles)
    result = run_backtest(candles, signals, initial_capital=10000.0, risk_per_trade=0.01)
    assert result.initial_capital == 10000.0
    assert isinstance(result.win_rate, float)
    assert isinstance(result.profit_factor, float)


def test_fvg_detects_signal():
    candles = _make_candles()
    signals = detect_fvg(candles)
    # At least one signal should be detected in this pattern
    assert len(signals) >= 1
    assert signals[0]["direction"] == "long"
    assert "type" in signals[0]
    assert signals[0]["type"] == "fvg_bullish"