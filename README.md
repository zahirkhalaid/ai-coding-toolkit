# AI Coding Toolkit

A starter kit for **vibe coding with AI and tools** — build, test, and iterate software using AI agents plus CLI tooling instead of writing every line by hand.

## What this is

This repo demonstrates a workflow where an AI writes the code and a human drives it with tools (terminal, git, package manager, test runner). It includes:

- A working Python backtesting engine
- An ICT-style signal detector (FVG, order block, liquidity sweep)
- A CLI to run strategies and export results
- AI prompt templates for generating new strategies
- Tests and a config-driven setup

## Quick start

```bash
# Install dependencies
pip install -e .

# Run the built-in example strategy
python -m ai_coding_toolkit run examples/ict_fvg_strategy.yaml

# Run tests
pytest

# Generate a new strategy with AI (see ai_prompts/)
```

## Project layout

```
ai-coding-toolkit/
├── README.md
├── WORKFLOW.md          # How to use AI + tools to build features
├── pyproject.toml
├── ai_prompts/          # Prompt templates for AI code generation
│   ├── strategy_generator.md
│   ├── backtest_reviewer.md
│   └── risk_manager.md
├── src/ai_coding_toolkit/
│   ├── __init__.py
│   ├── cli.py           # Command-line entry point
│   ├── backtest.py      # Backtesting engine
│   ├── signals.py       # Signal detection (FVG, OB, sweep)
│   └── risk.py          # Position sizing & risk checks
├── config/
│   ├── settings.yaml    # Global settings
│   └── strategy.yaml    # Strategy parameters
├── tests/
│   ├── test_backtest.py
│   └── test_signals.py
├── examples/
│   └── ict_fvg_strategy.yaml
└── data/
    └── sample_candles.csv
```

## The vibe-coding workflow

See `WORKFLOW.md` for the step-by-step loop of: prompt AI → run code → test → fix → repeat.

## License

MIT