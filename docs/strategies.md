# Trading Strategies Documentation

## Overview

This document describes the trading strategies implemented in this repository.

## Base Strategy

All strategies inherit from `BaseStrategy` class which provides:
- Strategy initialization with parameters
- Signal generation interface
- Backtesting framework

## Implemented Strategies

### 1. Simple Moving Average (SMA) Crossover

**File**: `src/strategies.py`

**Description**: A classic momentum strategy that generates buy signals when a short-term moving average crosses above a long-term moving average, and sell signals when it crosses below.

**Parameters**:
- `short_window` (int): Period for short-term MA (default: 20)
- `long_window` (int): Period for long-term MA (default: 50)

**Signals**:
- `1` (Buy): Short MA > Long MA
- `-1` (Sell): Short MA < Long MA
- `0` (Hold): No change in position

**Example**:
```python
from src.strategies import SimpleMovingAverageCrossover

strategy = SimpleMovingAverageCrossover(
    short_window=20,
    long_window=50
)

signals = strategy.generate_signals(data)
```

**Pros**:
- Simple and easy to understand
- Works well in trending markets
- Low computational requirements

**Cons**:
- Lags price action
- Performs poorly in ranging markets
- Many false signals in choppy conditions

## Developing New Strategies

To create a new strategy:

1. Inherit from `BaseStrategy`
2. Implement `generate_signals()` method
3. Implement `backtest()` method (optional)
4. Add tests in `tests/test_strategies.py`

Example template:
```python
class MyStrategy(BaseStrategy):
    def __init__(self, param1, param2):
        super().__init__(
            name="MyStrategy",
            params={"param1": param1, "param2": param2}
        )
        self.param1 = param1
        self.param2 = param2
    
    def generate_signals(self, data):
        signals = data.copy()
        # Your logic here
        signals['signal'] = 0  # Calculate signals
        return signals
```

## Backtesting Guidelines

When backtesting strategies:

1. Use realistic assumptions (commissions, slippage)
2. Avoid look-ahead bias
3. Consider transaction costs
4. Test on out-of-sample data
5. Perform walk-forward analysis
6. Calculate risk-adjusted returns (Sharpe ratio, etc.)

## Risk Management

Always implement proper risk management:
- Position sizing (e.g., Kelly Criterion, Fixed Fractional)
- Stop losses
- Portfolio diversification
- Maximum drawdown limits
