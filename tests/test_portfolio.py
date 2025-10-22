"""
Tests for portfolio management.
"""

import pytest
from src.portfolio import Portfolio


class TestPortfolio:
    """Tests for Portfolio class"""
    
    def test_initialization(self):
        """Test portfolio initialization"""
        portfolio = Portfolio(initial_capital=100000)
        assert portfolio.initial_capital == 100000
        assert portfolio.cash == 100000
        assert len(portfolio.positions) == 0
        
    def test_buy_order(self):
        """Test buying shares"""
        portfolio = Portfolio(initial_capital=100000)
        success = portfolio.buy("AAPL", 10, 150.0)
        
        assert success is True
        assert portfolio.cash == 98500  # 100000 - (10 * 150)
        assert portfolio.positions["AAPL"] == 10
        assert len(portfolio.history) == 1
        
    def test_buy_insufficient_funds(self):
        """Test buying with insufficient funds"""
        portfolio = Portfolio(initial_capital=1000)
        success = portfolio.buy("AAPL", 100, 150.0)
        
        assert success is False
        assert portfolio.cash == 1000  # No change
        assert "AAPL" not in portfolio.positions
        
    def test_sell_order(self):
        """Test selling shares"""
        portfolio = Portfolio(initial_capital=100000)
        portfolio.buy("AAPL", 10, 150.0)
        success = portfolio.sell("AAPL", 5, 160.0)
        
        assert success is True
        assert portfolio.cash == 98500 + 800  # Initial - buy + sell
        assert portfolio.positions["AAPL"] == 5
        
    def test_sell_insufficient_shares(self):
        """Test selling more shares than owned"""
        portfolio = Portfolio(initial_capital=100000)
        portfolio.buy("AAPL", 10, 150.0)
        success = portfolio.sell("AAPL", 20, 160.0)
        
        assert success is False
        assert portfolio.positions["AAPL"] == 10  # No change
        
    def test_portfolio_value(self):
        """Test portfolio value calculation"""
        portfolio = Portfolio(initial_capital=100000)
        portfolio.buy("AAPL", 10, 150.0)
        portfolio.buy("GOOGL", 5, 2000.0)
        
        prices = {"AAPL": 160.0, "GOOGL": 2100.0}
        value = portfolio.get_portfolio_value(prices)
        
        # Cash: 100000 - 1500 - 10000 = 88500
        # Positions: 10 * 160 + 5 * 2100 = 1600 + 10500 = 12100
        # Total: 88500 + 12100 = 100600
        assert value == 100600
        
    def test_returns(self):
        """Test returns calculation"""
        portfolio = Portfolio(initial_capital=100000)
        returns = portfolio.get_returns(110000)
        assert returns == 10.0  # 10% return
