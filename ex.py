from vnstock.explorer.misc import *
import pandas as pd
from datetime import datetime, timedelta
import time

# Test single date
single_rate = vcb_exchange_rate(date='2024-05-25')
print("Single date result:")
print(single_rate.head())

def get_exchange_rates_for_date_range(start_date_str, end_date_str, interval_days=7, delay_seconds=2):
    """
    Fetch VCB exchange rates for a range of dates with rate limiting.
    
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
        Combined DataFrame with exchange rates for the date range
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # Initialize an empty list to store DataFrames
    all_rates = []
    
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
            # Fetch exchange rates for the current date
            call_count += 1
            print(f"[{call_count}/{total_calls}] Fetching exchange rates for {date_str}...")
            rates = vcb_exchange_rate(date=date_str)
            
            # Check if we got valid data
            if not rates.empty:
                # Append to the list
                all_rates.append(rates)
                print(f"  Retrieved {len(rates)} records")
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
    if all_rates:
        exchange_rates = pd.concat(all_rates, ignore_index=True)
        return exchange_rates
    else:
        print("No data was fetched for the specified date range.")
        return pd.DataFrame()

# Test the function with a date range
start_date = "2025-03-20"
end_date = "2025-03-27"  # Today's date

print("\nFetching exchange rates for date range:")
exchange_rates = get_exchange_rates_for_date_range(start_date, end_date, interval_days=2, delay_seconds=2)

# Display the results
if not exchange_rates.empty:
    print(f"\nFetched {len(exchange_rates)} exchange rate records from {start_date} to {end_date}")
    print("\nFirst few records:")
    print(exchange_rates.head())
    
    print("\nLast few records:")
    print(exchange_rates.tail())
    
    # Save to CSV
    output_file = "exchange_rates.csv"
    exchange_rates.to_csv(output_file, index=False)
    print(f"\nExchange rates saved to {output_file}")