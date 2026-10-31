# Strategy Generator Prompt

Use this prompt with your AI assistant to generate a new trading strategy
for this toolkit. Paste it into your chat, then copy the AI's code into
`src/ai_coding_toolkit/`.

---

You are an expert quant developer. I am building a trading backtesting
toolkit in Python. The project structure is:

- `src/ai_coding_toolkit/backtest.py` — has `run_backtest(candles, signals, ...)`
  and `Candle` dataclass (timestamp, open, high, low, close, volume)
- `src/ai_coding_toolkit/signals.py` — detector functions return lists of
  signal dicts with keys: index, direction ("long"/"short"), entry_price,
  stop_loss, take_profit, type
- `src/ai_coding_toolkit/risk.py` — `position_size(equity, risk_per_trade, stop_distance)`
- `src/ai_coding_toolkit/cli.py` — CLI entry point

Task: Write a NEW signal detector function for [STRATEGY NAME HERE].

Requirements:
1. Function name: `detect_[strategy_name](candles: list[Candle]) -> list[dict]`
2. Follow the exact pattern of existing detectors in signals.py
3. Each signal dict must have: index, direction, entry_price, stop_loss, take_profit, type
4. Use only the Python standard library (no pandas/numpy in the detector)
5. Add clear comments explaining the logic
6. Include type hints

After writing the function, also write a short test in `tests/test_signals.py`
that verifies the detector produces at least one signal on sample data.

Output ONLY the Python code for the new function and the test — no explanation.