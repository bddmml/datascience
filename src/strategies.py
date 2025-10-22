"""
Trading Strategies Module

Contains base classes and implementations for various trading strategies.
"""

from typing import Optional, Dict, Any
import pandas as pd
import numpy as np


class BaseStrategy:
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize a trading strategy.
        
        Args:
            name: Strategy name
            params: Strategy parameters
        """
        self.name = name
        self.params = params or {}
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on market data.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with signals column (1=buy, -1=sell, 0=hold)
        """
        raise NotImplementedError("Subclasses must implement generate_signals")
        
    def backtest(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Backtest the strategy on historical data.
        
        Args:
            data: Historical OHLCV data
            
        Returns:
            Dictionary of performance metrics
        """
        raise NotImplementedError("Subclasses must implement backtest")


class SimpleMovingAverageCrossover(BaseStrategy):
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        """
        Initialize SMA Crossover Strategy.
        
        Args:
            short_window: Short-term SMA period
            long_window: Long-term SMA period
        """
        super().__init__(
            name="SMA_Crossover",
            params={"short_window": short_window, "long_window": long_window}
        )
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals based on SMA crossover.
        
        Args:
            data: DataFrame with 'close' price column
            
        Returns:
            DataFrame with signals
        """
        signals = data.copy()
        
        # Calculate moving averages
        signals['short_ma'] = signals['close'].rolling(
            window=self.short_window, min_periods=1
        ).mean()
        signals['long_ma'] = signals['close'].rolling(
            window=self.long_window, min_periods=1
        ).mean()
        
        # Generate signals
        signals['signal'] = 0
        signals.loc[signals['short_ma'] > signals['long_ma'], 'signal'] = 1
        signals.loc[signals['short_ma'] < signals['long_ma'], 'signal'] = -1
        
        return signals
