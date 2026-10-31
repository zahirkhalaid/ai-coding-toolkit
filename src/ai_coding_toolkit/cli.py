"""Command-line interface for the AI Coding Toolkit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .backtest import load_candles, run_backtest
from .signals import detect_fvg, detect_order_block, detect_liquidity_sweep
from .risk import check_drawdown


def _build_signals(candles, strategy: str):
    if strategy == "fvg":
        return detect_fvg(candles)
    if strategy == "ob":
        return detect_order_block(candles)
    if strategy == "sweep":
        return detect_liquidity_sweep(candles)
    if strategy == "all":
        return (
            detect_fvg(candles)
            + detect_order_block(candles)
            + detect_liquidity_sweep(candles)
        )
    raise ValueError(f"Unknown strategy: {strategy}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run AI-generated trading strategies on candle data"
    )
    parser.add_argument("data", help="Path to OHLC CSV file")
    parser.add_argument(
        "--strategy",
        choices=["fvg", "ob", "sweep", "all"],
        default="all",
        help="Signal strategy to use",
    )
    parser.add_argument(
        "--capital", type=float, default=10000.0, help="Initial capital"
    )
    parser.add_argument(
        "--risk", type=float, default=0.01, help="Risk per trade (fraction)"
    )
    args = parser.parse_args(argv)

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        return 1

    candles = load_candles(data_path)
    print(f"Loaded {len(candles)} candles from {data_path}")

    signals = _build_signals(candles, args.strategy)
    print(f"Generated {len(signals)} signals using '{args.strategy}' strategy")

    result = run_backtest(
        candles,
        signals,
        initial_capital=args.capital,
        risk_per_trade=args.risk,
    )

    print("\n=== Backtest Results ===")
    print(f"Trades:           {len(result.trades)}")
    print(f"Win rate:         {result.win_rate:.2%}")
    print(f"Profit factor:    {result.profit_factor:.2f}")
    print(f"Max drawdown:     {result.max_drawdown:.2%}")
    print(f"Total PnL:        {result.total_pnl:.2f}")
    print(f"Final equity:     {result.final_equity:.2f}")

    if check_drawdown(result.equity_curve, 0.20):
        print("\nWARNING: Max drawdown exceeds 20%")

    print("\nRecent trades:")
    for t in result.trades[-5:]:
        pnl = t.pnl or 0.0
        print(
            f"  {t.entry_time} {t.direction} @ {t.entry_price:.2f} -> "
            f"{t.exit_price or 0:.2f} PnL={pnl:.2f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())