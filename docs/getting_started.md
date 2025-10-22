# Getting Started with Quant Trading Analysis

## Installation

1. Clone this repository (requires access to private repo)
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Fetching Data

```python
from src.data_loader import DataLoader

# Initialize data loader
loader = DataLoader(data_source="yahoo")

# Fetch historical data
data = loader.fetch_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01"
)

print(data.head())
```

### Running a Strategy

```python
from src.strategies import SimpleMovingAverageCrossover

# Initialize strategy
strategy = SimpleMovingAverageCrossover(
    short_window=20,
    long_window=50
)

# Generate signals
signals = strategy.generate_signals(data)

# View signals
print(signals[['close', 'short_ma', 'long_ma', 'signal']].tail())
```

### Portfolio Management

```python
from src.portfolio import Portfolio

# Create portfolio
portfolio = Portfolio(initial_capital=100000)

# Execute trades
portfolio.buy("AAPL", 10, 150.50)
portfolio.sell("AAPL", 5, 155.00)

# Check portfolio value
current_prices = {"AAPL": 160.00}
value = portfolio.get_portfolio_value(current_prices)
print(f"Portfolio Value: ${value:,.2f}")
```

## Next Steps

- Explore the `notebooks/` directory for analysis examples
- Read the strategy documentation in `docs/strategies.md`
- Check configuration options in `config/`
- Run tests with `pytest tests/`

## Best Practices

1. **Version Control**: Always commit code changes with descriptive messages
2. **Testing**: Write tests for new strategies before deploying
3. **Documentation**: Document your strategies and findings
4. **Risk Management**: Never risk more than you can afford to lose
5. **Paper Trading**: Test strategies with paper trading before real money
