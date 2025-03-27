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

# We'll use the percentage changes directly instead of calculating log returns
# This avoids issues with zero or negative values
daily_returns = returns_data

# Calculate annualized returns (252 trading days)
ann_returns = daily_returns.mean() * 252

# Calculate covariance matrix of returns (annualized)
cov_mat = daily_returns.cov() * 252

# Define the number of portfolios to simulate
num_port = 5000

# Initialize arrays for portfolio weights, returns, risk, and Sharpe ratios
all_wts = np.zeros((num_port, len(daily_returns.columns)))
port_returns = np.zeros(num_port)
port_risk = np.zeros(num_port)
sharpe_ratio = np.zeros(num_port)

# Simulate random portfolios
np.random.seed(42)
for i in range(num_port):
    # Generate random portfolio weights
    wts = np.random.uniform(size=len(daily_returns.columns))
    wts = wts / np.sum(wts)
    all_wts[i, :] = wts

    # Calculate portfolio return (using annualized returns)
    port_ret = np.sum(ann_returns * wts)
    port_returns[i] = port_ret

    # Calculate portfolio risk (standard deviation)
    port_sd = np.sqrt(np.dot(wts.T, np.dot(cov_mat, wts)))
    port_risk[i] = port_sd

    # Calculate Sharpe Ratio, assuming a risk-free rate of 0%
    sr = port_ret / port_sd if port_sd > 0 else 0
    sharpe_ratio[i] = sr

# Identify portfolios with max Sharpe ratio, max return, and minimum variance
max_sr_idx = sharpe_ratio.argmax()
max_ret_idx = port_returns.argmax()
min_var_idx = port_risk.argmin()

max_sr_ret = port_returns[max_sr_idx]
max_sr_risk = port_risk[max_sr_idx]
max_sr_w = all_wts[max_sr_idx, :]

max_ret_ret = port_returns[max_ret_idx]
max_ret_risk = port_risk[max_ret_idx]
max_ret_w = all_wts[max_ret_idx, :]

min_var_ret = port_returns[min_var_idx]
min_var_risk = port_risk[min_var_idx]
min_var_w = all_wts[min_var_idx, :]

# Print the results
print("\nOptimal Portfolio Results:")
print("Maximum Sharpe Ratio Portfolio:")
print(f"  Expected Return: {max_sr_ret:.4f}")
print(f"  Risk: {max_sr_risk:.4f}")
print(f"  Sharpe Ratio: {max_sr_ret/max_sr_risk:.4f}")
print("  Weights:")
for j, col in enumerate(daily_returns.columns):
    symbol = col.split('_close_pct_change')[0]
    print(f"    {symbol}: {max_sr_w[j]:.4f}")

print("\nMaximum Return Portfolio:")
print(f"  Expected Return: {max_ret_ret:.4f}")
print(f"  Risk: {max_ret_risk:.4f}")
print(f"  Sharpe Ratio: {max_ret_ret/max_ret_risk:.4f}")

print("\nMinimum Variance Portfolio:")
print(f"  Expected Return: {min_var_ret:.4f}")
print(f"  Risk: {min_var_risk:.4f}")
print(f"  Sharpe Ratio: {min_var_ret/min_var_risk:.4f}")