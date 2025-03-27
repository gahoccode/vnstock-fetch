# Vietnamese Stock Price Fetcher

A simple Python script to fetch and visualize historical stock prices for multiple Vietnamese companies using the vnstock library.

## Features

- Fetch historical stock data for multiple Vietnamese companies
- Generate visualizations of closing prices
- Save combined data to CSV for further analysis
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

After activating the virtual environment, run the script:

```bash
python fetch_stock_prices.py
```

The script will:
1. Fetch historical stock data for VNM, VHM, VIC, FPT, and MWG for the last 6 months
2. Display basic statistics for each stock
3. Generate and save a plot comparing closing prices
4. Save the combined data to a CSV file

## Customization

You can modify the script to:
- Change the list of stock symbols
- Adjust the date range
- Change the data resolution (e.g., from daily to weekly)
- Add additional analysis or visualizations

## Dependencies

- vnstock==3.2.2
- pandas>=2.2.0
- matplotlib>=3.10.0
- seaborn>=0.13.0
