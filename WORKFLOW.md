# Vibe Coding Workflow

How to build features with AI + tools, not by hand.

## The loop

1. **Prompt** — Ask the AI to write or modify code using a template from `ai_prompts/`.
2. **Run** — Execute the code in the terminal to see what happens.
3. **Test** — Run `pytest` to verify behavior.
4. **Fix** — Paste errors back to the AI; ask it to patch.
5. **Commit** — `git add -A && git commit` when it works.
6. **Repeat.**

## Example: add a new signal detector

```
# 1. Prompt the AI
"Write a Python function that detects fair value gaps (FVG) in OHLC candle data.
Return a list of dicts with keys: type, index, top, bottom, filled.
Follow the pattern in src/ai_coding_toolkit/signals.py."

# 2. Add it to src/ai_coding_toolkit/signals.py
# 3. Write a test in tests/test_signals.py
# 4. Run pytest
# 5. If red, paste the failure back to the AI and ask for a fix
# 6. Commit
```

## AI prompt templates

- `ai_prompts/strategy_generator.md` — generate a new trading strategy
- `ai_prompts/backtest_reviewer.md` — review backtest results for overfitting
- `ai_prompts/risk_manager.md` — add position sizing and drawdown guards

## Rules

- Never hand-write boilerplate; let the AI draft it, then you review.
- Every new feature needs a test before it's merged.
- Commit after each working iteration, not at the end.