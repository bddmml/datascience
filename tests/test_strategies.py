"""
Tests for trading strategies.
"""

import pytest
import pandas as pd
import numpy as np
from src.strategies import BaseStrategy, SimpleMovingAverageCrossover


class TestBaseStrategy:
    """Tests for BaseStrategy class"""
    
    def test_initialization(self):
        """Test strategy initialization"""
        strategy = BaseStrategy(name="Test", params={"param1": 10})
        assert strategy.name == "Test"
        assert strategy.params == {"param1": 10}
        
    def test_generate_signals_not_implemented(self):
        """Test that generate_signals raises NotImplementedError"""
        strategy = BaseStrategy(name="Test")
        with pytest.raises(NotImplementedError):
            strategy.generate_signals(pd.DataFrame())


class TestSimpleMovingAverageCrossover:
    """Tests for SMA Crossover strategy"""
    
    def test_initialization(self):
        """Test SMA strategy initialization"""
        strategy = SimpleMovingAverageCrossover(short_window=10, long_window=30)
        assert strategy.name == "SMA_Crossover"
        assert strategy.short_window == 10
        assert strategy.long_window == 30
        
    def test_generate_signals(self):
        """Test signal generation"""
        # Create sample data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        prices = np.linspace(100, 150, 100) + np.random.randn(100) * 5
        data = pd.DataFrame({'close': prices}, index=dates)
        
        strategy = SimpleMovingAverageCrossover(short_window=10, long_window=30)
        signals = strategy.generate_signals(data)
        
        # Check that signals are generated
        assert 'signal' in signals.columns
        assert 'short_ma' in signals.columns
        assert 'long_ma' in signals.columns
        
        # Check signal values are valid
        assert set(signals['signal'].unique()).issubset({-1, 0, 1})
