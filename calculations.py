"""
Stock Price Calculations Module

This module calculates percentage changes (returns) from close prices
using the combined_prices variable imported from test.py.
"""

import pandas as pd
import numpy as np

# Import combined_prices from test.py
from test import combined_prices


def calculate_returns():
    """
    Calculate percentage changes (returns) from close prices using the combined_prices variable.
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the percentage changes with time as index
    """
    # Make a copy to avoid modifying the original
    returns_data = combined_prices.copy()
    
    # Ensure time is in datetime format and sorted
    if 'time' in returns_data.columns:
        returns_data['time'] = pd.to_datetime(returns_data['time'])
        returns_data.sort_values('time', inplace=True)
        returns_data.set_index('time', inplace=True)
    
    # Calculate percentage change for each price column
    for column in returns_data.columns:
        if column != 'time':  # Exclude time column
            returns_data[f'{column}_pct_change'] = returns_data[column].pct_change()
    
    # Drop the original price columns
    price_columns = [col for col in returns_data.columns if not col.endswith('_pct_change')]
    returns_data = returns_data.drop(columns=price_columns)
    
    # Drop rows with NaN values
    returns_data = returns_data.dropna()
    
    # Keep time as index - do not reset
    return returns_data

returns_data = calculate_returns()

print(returns_data.head())
