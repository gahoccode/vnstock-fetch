"""
Streamlit App for Vietnamese Stock Portfolio Optimization

This app allows users to:
1. Input date range and stock symbols
2. Specify the number of portfolios to simulate
3. View the optimal portfolio results
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import importlib
import os

# Set page configuration
st.set_page_config(
    page_title="Vietnamese Stock Portfolio Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a title and description
st.title("Vietnamese Stock Portfolio Optimizer")
st.markdown("""
This application helps you optimize your Vietnamese stock portfolio by finding:
- Maximum Sharpe Ratio Portfolio (best risk-adjusted return)
- Maximum Return Portfolio
- Minimum Variance Portfolio (lowest risk)
""")

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Date range input
today = datetime.now()
default_start_date = today - timedelta(days=365)  # Default to 1 year ago
default_end_date = today

start_date = st.sidebar.date_input(
    "Start Date",
    value=default_start_date,
    min_value=datetime(2010, 1, 1),
    max_value=today
)

end_date = st.sidebar.date_input(
    "End Date",
    value=default_end_date,
    min_value=start_date,
    max_value=today
)

# Stock symbols input
default_symbols = "REE,FMC,DHC"
symbols_input = st.sidebar.text_input(
    "Stock Symbols (comma-separated)",
    value=default_symbols
)
symbols = [symbol.strip() for symbol in symbols_input.split(",")]

# Number of portfolios to simulate
num_port = st.sidebar.number_input(
    "Number of Portfolios to Simulate",
    min_value=1000,
    max_value=10000,
    value=5000,
    step=1000
)

# Function to run the analysis
def run_analysis():
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Update the symbols and date range in the global namespace
    status_text.text("Fetching historical stock data...")
    
    # Prepare the modified test.py code to run with our parameters
    import vnstock
    from vnstock import Quote
    
    # Dictionary to store historical data for each symbol
    all_historical_data = {}
    
    # Convert dates to string format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    interval = '1D'
    
    # Fetch historical data for each symbol
    for i, symbol in enumerate(symbols):
        try:
            status_text.text(f"Processing {symbol}...")
            quote = Quote(symbol=symbol)
            
            # Fetch historical price data
            historical_data = quote.history(
                start=start_date_str,
                end=end_date_str,
                interval=interval,
                to_df=True
            )
            
            if not historical_data.empty:
                all_historical_data[symbol] = historical_data
                st.sidebar.success(f"Successfully fetched {len(historical_data)} records for {symbol}")
            else:
                st.sidebar.warning(f"No historical data available for {symbol}")
        except Exception as e:
            st.sidebar.error(f"Error fetching data for {symbol}: {e}")
        
        # Update progress
        progress_bar.progress((i + 1) / len(symbols) * 0.5)
    
    # Check if we have data
    if not all_historical_data:
        st.error("No historical data was fetched for any symbol. Please check the symbols and try again.")
        return None, None
    
    # Create a combined DataFrame for close prices only
    combined_prices = pd.DataFrame()
    
    for symbol, data in all_historical_data.items():
        if not data.empty:
            # Extract time and close price
            temp_df = data[['time', 'close']].copy()
            temp_df.rename(columns={'close': f'{symbol}_close'}, inplace=True)
            
            if combined_prices.empty:
                combined_prices = temp_df
            else:
                combined_prices = pd.merge(combined_prices, temp_df, on='time', how='outer')
    
    # Sort by time
    if not combined_prices.empty:
        combined_prices = combined_prices.sort_values('time')
    
    status_text.text("Calculating portfolio returns...")
    progress_bar.progress(0.6)
    
    # Calculate returns using the logic from calculations.py
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
    
    status_text.text("Optimizing portfolios...")
    progress_bar.progress(0.7)
    
    # We'll use the percentage changes directly
    daily_returns = returns_data
    
    # Calculate annualized returns (252 trading days)
    ann_returns = daily_returns.mean() * 252
    
    # Calculate covariance matrix of returns (annualized)
    cov_mat = daily_returns.cov() * 252
    
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
        
        # Update progress periodically
        if i % (num_port // 10) == 0:
            progress_bar.progress(0.7 + (i / num_port) * 0.3)
    
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
    
    # Create results dictionary
    results = {
        'max_sharpe': {
            'return': max_sr_ret,
            'risk': max_sr_risk,
            'sharpe': max_sr_ret/max_sr_risk if max_sr_risk > 0 else 0,
            'weights': {daily_returns.columns[j].split('_close_pct_change')[0]: max_sr_w[j] for j in range(len(daily_returns.columns))}
        },
        'max_return': {
            'return': max_ret_ret,
            'risk': max_ret_risk,
            'sharpe': max_ret_ret/max_ret_risk if max_ret_risk > 0 else 0,
            'weights': {daily_returns.columns[j].split('_close_pct_change')[0]: max_ret_w[j] for j in range(len(daily_returns.columns))}
        },
        'min_variance': {
            'return': min_var_ret,
            'risk': min_var_risk,
            'sharpe': min_var_ret/min_var_risk if min_var_risk > 0 else 0,
            'weights': {daily_returns.columns[j].split('_close_pct_change')[0]: min_var_w[j] for j in range(len(daily_returns.columns))}
        }
    }
    
    # Create a DataFrame with all portfolios for the scatter plot
    portfolios_df = pd.DataFrame({
        'Return': port_returns,
        'Risk': port_risk,
        'Sharpe Ratio': sharpe_ratio
    })
    
    progress_bar.progress(1.0)
    status_text.text("Analysis complete!")
    
    return results, portfolios_df

# Run button
if st.sidebar.button("Run Analysis"):
    with st.spinner("Running portfolio optimization..."):
        results, portfolios_df = run_analysis()
        
        if results is not None:
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["Maximum Sharpe Ratio", "Maximum Return", "Minimum Variance"])
            
            with tab1:
                st.header("Maximum Sharpe Ratio Portfolio")
                st.subheader("Best Risk-Adjusted Return")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Expected Annual Return", f"{results['max_sharpe']['return']:.2%}")
                    st.metric("Annual Risk (Std Dev)", f"{results['max_sharpe']['risk']:.2%}")
                    st.metric("Sharpe Ratio", f"{results['max_sharpe']['sharpe']:.4f}")
                
                with col2:
                    st.subheader("Portfolio Weights")
                    weights_df = pd.DataFrame({
                        'Symbol': list(results['max_sharpe']['weights'].keys()),
                        'Weight': list(results['max_sharpe']['weights'].values())
                    })
                    weights_df['Weight'] = weights_df['Weight'].apply(lambda x: f"{x:.2%}")
                    st.dataframe(weights_df)
            
            with tab2:
                st.header("Maximum Return Portfolio")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Expected Annual Return", f"{results['max_return']['return']:.2%}")
                    st.metric("Annual Risk (Std Dev)", f"{results['max_return']['risk']:.2%}")
                    st.metric("Sharpe Ratio", f"{results['max_return']['sharpe']:.4f}")
                
                with col2:
                    st.subheader("Portfolio Weights")
                    weights_df = pd.DataFrame({
                        'Symbol': list(results['max_return']['weights'].keys()),
                        'Weight': list(results['max_return']['weights'].values())
                    })
                    weights_df['Weight'] = weights_df['Weight'].apply(lambda x: f"{x:.2%}")
                    st.dataframe(weights_df)
            
            with tab3:
                st.header("Minimum Variance Portfolio")
                st.subheader("Lowest Risk")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Expected Annual Return", f"{results['min_variance']['return']:.2%}")
                    st.metric("Annual Risk (Std Dev)", f"{results['min_variance']['risk']:.2%}")
                    st.metric("Sharpe Ratio", f"{results['min_variance']['sharpe']:.4f}")
                
                with col2:
                    st.subheader("Portfolio Weights")
                    weights_df = pd.DataFrame({
                        'Symbol': list(results['min_variance']['weights'].keys()),
                        'Weight': list(results['min_variance']['weights'].values())
                    })
                    weights_df['Weight'] = weights_df['Weight'].apply(lambda x: f"{x:.2%}")
                    st.dataframe(weights_df)
            
            # Display efficient frontier
            st.header("Efficient Frontier")
            st.write("Each point represents a simulated portfolio. The efficient frontier contains the optimal portfolios.")
            
            import altair as alt
            
            # Create a scatter plot of all portfolios
            chart = alt.Chart(portfolios_df).mark_circle(size=60).encode(
                x=alt.X('Risk', title='Risk (Annual Volatility)'),
                y=alt.Y('Return', title='Expected Return (Annual)'),
                color=alt.Color('Sharpe Ratio', scale=alt.Scale(scheme='viridis')),
                tooltip=['Return', 'Risk', 'Sharpe Ratio']
            ).properties(
                width=800,
                height=500,
                title='Portfolio Risk-Return Profile'
            ).interactive()
            
            # Add points for the three key portfolios
            key_portfolios = pd.DataFrame({
                'Portfolio': ['Max Sharpe', 'Max Return', 'Min Variance'],
                'Return': [results['max_sharpe']['return'], results['max_return']['return'], results['min_variance']['return']],
                'Risk': [results['max_sharpe']['risk'], results['max_return']['risk'], results['min_variance']['risk']]
            })
            
            highlight = alt.Chart(key_portfolios).mark_point(size=100, filled=True).encode(
                x='Risk',
                y='Return',
                color=alt.Color('Portfolio', scale=alt.Scale(domain=['Max Sharpe', 'Max Return', 'Min Variance'], 
                                                           range=['#ff7f0e', '#2ca02c', '#1f77b4'])),
                shape=alt.Shape('Portfolio', scale=alt.Scale(domain=['Max Sharpe', 'Max Return', 'Min Variance'], 
                                                           range=['triangle', 'square', 'circle'])),
                tooltip=['Portfolio', 'Return', 'Risk']
            )
            
            st.altair_chart(chart + highlight, use_container_width=True)

# Add instructions at the bottom
st.markdown("""
### How to use this app:
1. Set your desired date range in the sidebar
2. Enter the stock symbols you want to analyze (comma-separated)
3. Adjust the number of portfolios to simulate (more portfolios = more accurate results but slower)
4. Click "Run Analysis" to start the optimization process
5. View the results in the tabs above

### Notes:
- The app uses historical data to optimize portfolios, which may not predict future performance
- All returns are annualized (assuming 252 trading days per year)
- The Sharpe Ratio is calculated assuming a risk-free rate of 0%
""")

# Add a footer
st.markdown("""
---
Created with Streamlit using vnstock data
""")
