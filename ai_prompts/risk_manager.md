# Risk Manager Prompt

Use this prompt to add position sizing and drawdown guards to a strategy.

---

You are a risk management expert. Review the following strategy code:

{STRATEGY_CODE}

Add or improve:
1. Position sizing using `position_size(equity, risk_per_trade, stop_distance)`
2. Max drawdown circuit breaker using `check_drawdown(equity_curve, max_allowed)`
3. Per-trade risk cap (e.g. max 1% of equity per trade)
4. Daily loss limit
5. Maximum concurrent positions

Output the updated Python code with risk controls integrated.