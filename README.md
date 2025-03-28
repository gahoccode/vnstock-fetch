# Vietnamese Stock Price Fetcher

A Python toolkit for fetching, analyzing, and screening Vietnamese stock data using the vnstock library.

## Features

- Fetch historical stock data for multiple Vietnamese companies
- Screen stocks based on technical indicators
- Detect stocks that are "heating up" in the market
- Fetch company financial data and reports
- Generate visualizations of closing prices
- Save data to CSV for further analysis
- Display basic statistics for each stock

## Setup Instructions

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Portfolio Management

```bash
python calculations.py
```

### Stock Screening

```bash
python screener.py
```

The screener will:
1. Fetch data for all stocks on HOSE, HNX, and UPCOM exchanges
2. Identify stocks that are "heating up" based on technical indicators
3. Display the heating up stocks and save them to CSV

### Company Financial Data

```bash
python fs.py
```

This script demonstrates how to:
1. Fetch financial statements (balance sheet, income statement, cash flow)
2. Get company overview, profile, and shareholder information
3. Retrieve insider deals, subsidiaries, and officer information
4. Get company events, news, and dividend history

## Customization

You can modify the scripts to:
- Change the list of stock symbols
- Adjust the date range
- Change the data resolution (e.g., from daily to weekly)
- Add additional analysis or visualizations
- Create custom screening strategies

## Stock Screening Indicators

The vnstock screener provides a wide range of technical and fundamental indicators:

- Price vs Moving Averages (SMA5, SMA20, SMA50, SMA100)
- Volume Indicators (relative to SMAs, trading values)
- Momentum Indicators (RSI, MACD, relative strength)
- Trend Indicators (uptrend, breakout, continuous days)
- Technical Signals (Bollinger Bands, DMI)
- Price Growth (various timeframes)
- Fundamental Indicators (PE, PB, ROE, EPS)

For a complete list of available indicators and custom screening strategies, see [ScreenerDocs.md](ScreenerDocs.md).

## Dependencies

- vnstock==3.2.2
- pandas>=2.2.0
- matplotlib>=3.10.0
- seaborn>=0.13.0

