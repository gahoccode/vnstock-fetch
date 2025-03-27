from vnstock import Vnstock
from datetime import datetime, timedelta
import pandas as pd
import time
from vnstock.explorer.misc import *

source = 'VCI' # 'VCI' hoặc 'TCBS'

stock = Vnstock().stock(symbol='VN30F1M', source='VCI')
df = stock.quote.history(start='2020-01-01', end='2024-12-31')
# Đặt cột 'time' làm cột index
df.set_index('time', inplace=True)
#print(df.head())

# Function to fetch gold prices for a date range
def get_gold_prices_for_date_range(start_date_str, end_date_str, interval_days=7, delay_seconds=2):
    """
    Fetch gold prices for a range of dates with rate limiting.
    
    Parameters:
    -----------
    start_date_str : str
        Start date in 'YYYY-MM-DD' format
    end_date_str : str
        End date in 'YYYY-MM-DD' format
    interval_days : int
        Number of days between each data point (to avoid excessive API calls)
    delay_seconds : int
        Number of seconds to wait between API calls to respect rate limits
        
    Returns:
    --------
    pandas.DataFrame
        Combined DataFrame with gold prices for the date range
        
    Notes:
    ------
    This function returns a DataFrame named 'gold_prices' which can be used
    with other modules in the vnstock project that expect this variable name.
    The DataFrame contains columns including 'name', 'buy_price', 'sell_price', and 'date'.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # Initialize an empty list to store DataFrames
    all_prices = []
    
    # Calculate total number of API calls
    total_days = (end_date - start_date).days
    total_calls = (total_days // interval_days) + 1
    
    print(f"Will make approximately {total_calls} API calls with {delay_seconds} second delay between calls")
    print(f"Estimated completion time: {total_calls * delay_seconds} seconds")
    
    # Loop through the date range with the specified interval
    current_date = start_date
    call_count = 0
    
    while current_date <= end_date:
        # Convert current date to string format
        date_str = current_date.strftime("%Y-%m-%d")
        
        try:
            # Fetch gold prices for the current date
            call_count += 1
            print(f"[{call_count}/{total_calls}] Fetching gold prices for {date_str}...")
            prices = sjc_gold_price(date=date_str)
            
            # Check if we got valid data
            if not prices.empty:
                # Append to the list
                all_prices.append(prices)
                print(f"  Retrieved {len(prices)} records")
            else:
                print(f"  No data available for {date_str}")
            
        except Exception as e:
            print(f"  Error fetching data for {date_str}: {e}")
        
        # Move to the next date
        current_date += timedelta(days=interval_days)
        
        # Add delay to respect rate limits (if not the last request)
        if current_date <= end_date:
            print(f"  Waiting {delay_seconds} seconds to respect API rate limits...")
            time.sleep(delay_seconds)
    
    # Combine all DataFrames
    if all_prices:
        gold_prices = pd.concat(all_prices, ignore_index=True)
        return gold_prices
    else:
        print("No data was fetched for the specified date range.")
        return pd.DataFrame()

def calculate_price_spread(df):
    """
    Calculate the spread between sell price and buy price.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing 'buy_price' and 'sell_price' columns
        
    Returns:
    --------
    pandas.DataFrame
        Original DataFrame with an additional 'price_spread' column
    """
    if 'buy_price' in df.columns and 'sell_price' in df.columns:
        # Create a copy to avoid SettingWithCopyWarning
        result_df = df.copy()
        
        # Calculate the spread (sell price - buy price)
        result_df['price_spread'] = result_df['sell_price'] - result_df['buy_price']
        
        return result_df
    else:
        print("Error: DataFrame must contain 'buy_price' and 'sell_price' columns")
        return df

# Define the date range
start_date = "2025-01-01"
end_date = "2025-03-27"  # Today's date

# Fetch gold prices for the date range with a 14-day interval and 3-second delay between requests
# Increased interval and delay to be more conservative with API usage
gold_prices = get_gold_prices_for_date_range(start_date, end_date, interval_days=14, delay_seconds=3)

# Display the results
if not gold_prices.empty:
    # Calculate price spread
    gold_prices = calculate_price_spread(gold_prices)
    
    print(f"\nFetched {len(gold_prices)} gold price records from {start_date} to {end_date}")
    print("\nFirst few records:")
    print(gold_prices.head())
    
    print("\nLast few records:")
    print(gold_prices.tail())
    
    # Save to CSV
    output_file = "gold_prices.csv"
    gold_prices.to_csv(output_file, index=False)
    print(f"\nGold prices saved to {output_file}")