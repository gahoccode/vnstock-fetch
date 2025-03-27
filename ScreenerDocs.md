# VNStock Screener Documentation

## Technical Indicators Available in VNStock Screener

The VNStock screener provides a comprehensive set of technical and fundamental indicators that can be used for stock screening and analysis. Below is a categorized list of the available indicators.

### Price vs Moving Averages
- `price_vs_sma5` - Price relative to 5-day Simple Moving Average
- `price_vs_sma10` - Price relative to 10-day Simple Moving Average
- `price_vs_sma20` - Price relative to 20-day Simple Moving Average
- `price_vs_sma50` - Price relative to 50-day Simple Moving Average
- `price_vs_sma100` - Price relative to 100-day Simple Moving Average

### Volume Indicators
- `vol_vs_sma5` - Volume relative to 5-day average volume
- `vol_vs_sma10` - Volume relative to 10-day average volume
- `vol_vs_sma20` - Volume relative to 20-day average volume
- `vol_vs_sma50` - Volume relative to 50-day average volume
- `avg_trading_value_5d` - Average trading value over 5 days
- `avg_trading_value_10d` - Average trading value over 10 days
- `avg_trading_value_20d` - Average trading value over 20 days
- `total_trading_value` - Total trading value
- `foreign_vol_pct` - Foreign volume percentage

### Momentum Indicators
- `rsi14` - 14-day Relative Strength Index
- `rsi14_status` - RSI status (overbought/oversold)
- `macd_histogram` - MACD histogram value
- `relative_strength_3d` - 3-day relative strength
- `rel_strength_1m` - 1-month relative strength
- `rel_strength_3m` - 3-month relative strength
- `rel_strength_1y` - 1-year relative strength

### Trend Indicators
- `uptrend` - Whether the stock is in an uptrend
- `num_increase_continuous_day` - Number of consecutive up days
- `num_decrease_continuous_day` - Number of consecutive down days
- `breakout` - Breakout status
- `price_break_out52_week` - Price breaking out of 52-week high
- `price_wash_out52_week` - Price washing out to 52-week low
- `heating_up` - Stock showing sudden momentum ("Tăng nóng")

### Technical Signals
- `bolling_band_signal` - Bollinger Band signal
- `dmi_signal` - Directional Movement Index signal
- `sar_vs_macd_hist` - SAR vs MACD histogram
- `tcbs_recommend` - TCBS recommendation
- `tcbs_buy_sell_signal` - TCBS buy/sell signal

### Price Growth
- `price_growth_1w` - 1-week price growth
- `price_growth_1m` - 1-month price growth
- `prev_1d_growth_pct` - Previous 1-day growth percentage
- `prev_1m_growth_pct` - Previous 1-month growth percentage
- `prev_1y_growth_pct` - Previous 1-year growth percentage
- `prev_5y_growth_pct` - Previous 5-year growth percentage
- `pct_1y_from_peak` - Percentage down from 1-year peak
- `pct_away_from_hist_peak` - Percentage away from historical peak
- `pct_1y_from_bottom` - Percentage up from 1-year bottom
- `pct_off_hist_bottom` - Percentage up from historical bottom

### Fundamental Indicators
- `market_cap` - Market capitalization
- `pe` - Price to Earnings ratio
- `pb` - Price to Book ratio
- `ev_ebitda` - Enterprise Value to EBITDA
- `dividend_yield` - Dividend yield
- `roe` - Return on Equity
- `eps` - Earnings Per Share
- `eps_growth_1y` - 1-year EPS growth
- `eps_growth_5y` - 5-year EPS growth
- `revenue_growth_1y` - 1-year revenue growth
- `revenue_growth_5y` - 5-year revenue growth
- `gross_margin` - Gross margin
- `net_margin` - Net margin
- `doe` - Debt to Equity ratio

### Other Indicators
- `stock_rating` - Overall stock rating
- `business_operation` - Business operation rating
- `business_model` - Business model rating
- `financial_health` - Financial health rating
- `alpha` - Alpha value
- `beta` - Beta value
- `active_buy_pct` - Active buy percentage
- `strong_buy_pct` - Strong buy percentage
- `high_vol_match` - High volume match
- `forecast_vol_ratio` - Forecast volume ratio
- `foreign_transaction` - Foreign transaction
- `foreign_buysell_20s` - Foreign buy/sell in last 20 sessions
- `has_financial_report` - Has recent financial report
- `free_transfer_rate` - Free transfer rate
- `net_cash_per_market_cap` - Net cash per market cap
- `net_cash_per_total_assets` - Net cash per total assets
- `profit_last_4q` - Profit in last 4 quarters
- `last_quarter_revenue_growth` - Last quarter revenue growth
- `second_quarter_revenue_growth` - Second last quarter revenue growth
- `last_quarter_profit_growth` - Last quarter profit growth
- `second_quarter_profit_growth` - Second last quarter profit growth

## "Heating Up" Stock Detection

The VNStock screener identifies "heating up" stocks primarily based on:

1. **Significant price increase in the previous trading session**
   - Indicated by `heating_up` column with value: `{'vi': 'Tăng nóng vào phiên hôm trước', 'en': 'Overheated in previous trading session'}`

2. **Price above key moving averages**
   - 100% of heating up stocks are above their 20-day SMA
   - ~89% of heating up stocks are above their 50-day SMA
   - ~89% of heating up stocks are above their 100-day SMA

This combination of recent price surge and position above key moving averages indicates strong momentum and is used to flag stocks that are "heating up" in the market.

## Usage Example

```python
from vnstock import Screener
from vnstock import Vnstock
import pandas as pd

# Get screener data
stock = Vnstock().stock(symbol='VCI', source='VCI')
screener_df = stock.screener.stock(params={"exchangeName": "HOSE,HNX,UPCOM"}, limit=1700)

# Find heating up stocks
heating_up_stocks = screener_df[pd.notna(screener_df['heating_up'])]

# Display results
print(f"Found {len(heating_up_stocks)} heating up stocks")
print(heating_up_stocks[['ticker', 'exchange', 'price', 'change_percent']].head(10))

# Save to CSV for further analysis
heating_up_stocks.to_csv("heating_up_stocks.csv", index=False)
```

## Custom Screening Strategies

You can create custom screening strategies by combining multiple indicators. Here are some examples:

### Momentum Strategy
```python
# Find stocks with strong momentum
momentum_stocks = screener_df[
    (screener_df['price_vs_sma20'].str.contains('trên', na=False)) &  # Price above SMA20
    (screener_df['price_vs_sma50'].str.contains('trên', na=False)) &  # Price above SMA50
    (screener_df['rsi14'] > 50) &                                     # RSI above 50
    (screener_df['change_percent'] > 0)                               # Positive daily change
]
```

### Volume Breakout Strategy
```python
# Find stocks with volume breakouts
volume_breakout = screener_df[
    (screener_df['vol_vs_sma20'].str.contains('trên', na=False)) &    # Volume above 20-day average
    (screener_df['price_vs_sma20'].str.contains('trên', na=False)) &  # Price above SMA20
    (screener_df['num_increase_continuous_day'] >= 2)                 # At least 2 consecutive up days
]
```

### Value Strategy
```python
# Find value stocks
value_stocks = screener_df[
    (screener_df['pe'] < 15) &                                        # Low P/E ratio
    (screener_df['pb'] < 1.5) &                                       # Low P/B ratio
    (screener_df['dividend_yield'] > 3) &                             # Good dividend yield
    (screener_df['roe'] > 15)                                         # Strong ROE
]
