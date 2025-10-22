"""
Portfolio Management Module

Handles position sizing, risk management, and portfolio tracking.
"""

from typing import Dict, List, Optional
import pandas as pd
import numpy as np


class Portfolio:
    """Portfolio management class"""
    
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initialize a portfolio.
        
        Args:
            initial_capital: Starting capital in base currency
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, float] = {}
        self.history: List[Dict] = []
        
    def get_portfolio_value(self, prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            prices: Current prices for each symbol
            
        Returns:
            Total portfolio value
        """
        position_value = sum(
            quantity * prices.get(symbol, 0)
            for symbol, quantity in self.positions.items()
        )
        return self.cash + position_value
        
    def buy(self, symbol: str, quantity: float, price: float) -> bool:
        """
        Execute a buy order.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            price: Price per share
            
        Returns:
            True if order executed successfully
        """
        cost = quantity * price
        
        if cost > self.cash:
            return False
            
        self.cash -= cost
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        
        self.history.append({
            'action': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'cost': cost
        })
        
        return True
        
    def sell(self, symbol: str, quantity: float, price: float) -> bool:
        """
        Execute a sell order.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            price: Price per share
            
        Returns:
            True if order executed successfully
        """
        if self.positions.get(symbol, 0) < quantity:
            return False
            
        proceeds = quantity * price
        self.cash += proceeds
        self.positions[symbol] -= quantity
        
        if self.positions[symbol] == 0:
            del self.positions[symbol]
            
        self.history.append({
            'action': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'proceeds': proceeds
        })
        
        return True
        
    def get_returns(self, current_value: float) -> float:
        """
        Calculate portfolio returns.
        
        Args:
            current_value: Current portfolio value
            
        Returns:
            Returns as percentage
        """
        return ((current_value - self.initial_capital) / self.initial_capital) * 100
