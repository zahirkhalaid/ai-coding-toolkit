"""AI Coding Toolkit — core modules."""

from .backtest import run_backtest, load_candles
from .signals import detect_fvg, detect_order_block, detect_liquidity_sweep
from .risk import position_size, check_drawdown

__version__ = "0.1.0"

__all__ = [
    "run_backtest",
    "load_candles",
    "detect_fvg",
    "detect_order_block",
    "detect_liquidity_sweep",
    "position_size",
    "check_drawdown",
]