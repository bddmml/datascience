"""
Data Loading and Preprocessing Module

Handles fetching and preprocessing financial data from various sources.
"""

from typing import Optional, List
import pandas as pd
from datetime import datetime, timedelta


class DataLoader:
    """Class for loading and managing financial data"""
    
    def __init__(self, data_source: str = "yahoo"):
        """
        Initialize the data loader.
        
        Args:
            data_source: Source for data ('yahoo', 'alpha_vantage', etc.)
        """
        self.data_source = data_source
        
    def fetch_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data for a given symbol.
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval: Data interval (1d, 1h, etc.)
            
        Returns:
            DataFrame with OHLCV data
        """
        if self.data_source == "yahoo":
            return self._fetch_yahoo_data(symbol, start_date, end_date, interval)
        else:
            raise ValueError(f"Unsupported data source: {self.data_source}")
            
    def _fetch_yahoo_data(
        self,
        symbol: str,
        start_date: Optional[str],
        end_date: Optional[str],
        interval: str
    ) -> pd.DataFrame:
        """Fetch data from Yahoo Finance"""
        try:
            import yfinance as yf
            
            # Set default dates if not provided
            if end_date is None:
                end_date = datetime.now().strftime("%Y-%m-%d")
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
            # Download data
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            # Standardize column names
            data.columns = data.columns.str.lower()
            
            return data
            
        except ImportError:
            raise ImportError("yfinance is required. Install with: pip install yfinance")
            
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess and clean the data.
        
        Args:
            data: Raw OHLCV data
            
        Returns:
            Cleaned DataFrame
        """
        # Remove duplicates
        data = data.drop_duplicates()
        
        # Handle missing values
        data = data.fillna(method='ffill')
        
        # Sort by date
        data = data.sort_index()
        
        return data
