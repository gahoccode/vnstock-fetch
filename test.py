from vnstock import Quote
import pandas as pd

# Define the symbols you want to fetch data for
symbols = ['REE', 'FMC', 'DHC']
print(f"Fetching historical price data for: {symbols}")

# Dictionary to store historical data for each symbol
all_historical_data = {}

# Set date range
start_date = '2024-01-01'
end_date = '2025-03-19'
interval = '1D'

# Fetch historical data for each symbol
for symbol in symbols:
    try:
        print(f"\nProcessing {symbol}...")
        quote = Quote(symbol=symbol)
        
        # Fetch historical price data
        historical_data = quote.history(
            start=start_date,
            end=end_date,
            interval=interval,
            to_df=True
        )
        
        if not historical_data.empty:
            all_historical_data[symbol] = historical_data
            print(f"Successfully fetched {len(historical_data)} records for {symbol}")
        else:
            print(f"No historical data available for {symbol}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Export all historical data to a single CSV file
if all_historical_data:
    # Create a combined DataFrame with all data
    combined_data = pd.DataFrame()
    
    for symbol, data in all_historical_data.items():
        if not data.empty:
            # Make a copy of the data and rename columns to include symbol
            temp_df = data.copy()
            # Keep 'time' column as is for merging
            for col in temp_df.columns:
                if col != 'time':
                    temp_df.rename(columns={col: f'{symbol}_{col}'}, inplace=True)
            
            if combined_data.empty:
                combined_data = temp_df
            else:
                combined_data = pd.merge(combined_data, temp_df, on='time', how='outer')
    
    # Sort by time
    if not combined_data.empty:
        combined_data = combined_data.sort_values('time')
        
        # Display sample of combined data
        print("\nSample of combined data:")
        print(combined_data.head(3))
        
        # Export combined data to CSV
        combined_csv_filename = 'all_historical_data.csv'
        combined_data.to_csv(combined_csv_filename, index=False, encoding='utf-8-sig')
        print(f"\nAll historical data exported to {combined_csv_filename}")
    
    # Also create a combined DataFrame for close prices only (for comparison purposes)
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
        
        # Export combined close prices to CSV
        combined_close_csv_filename = 'combined_close_prices.csv'
        combined_prices.to_csv(combined_close_csv_filename, index=False, encoding='utf-8-sig')
        print(f"Combined close price data exported to {combined_close_csv_filename}")
else:
    print("No historical data was fetched for any symbol.")