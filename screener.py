from vnstock import Screener
from vnstock import Vnstock
import pandas as pd

symbol='VCI'
source='VCI'
def get_screener_data(exchange_names="HOSE,HNX,UPCOM", limit=1700):
    """
    Fetch stock screener data from VCI source.
    
    Parameters:
    -----------
    exchange_names : str
        Comma-separated list of exchanges to include (default: "HOSE,HNX,UPCOM")
    limit : int
        Maximum number of stocks to return (default: 1700)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing screener data for all stocks
    """
    stock = Vnstock().stock(symbol=symbol, source=source)
    screener_df = stock.screener.stock(params={"exchangeName": exchange_names}, limit=limit)
    return screener_df

def find_heating_up_stocks(screener_df=None, exchange_names="HOSE,HNX,UPCOM", limit=1700):
    """
    Find stocks that have any non-None values in the heating_up column.
    
    Parameters:
    -----------
    screener_df : pandas.DataFrame, optional
        Pre-fetched screener data. If None, data will be fetched (default: None)
    exchange_names : str
        Comma-separated list of exchanges to include if fetching data (default: "HOSE,HNX,UPCOM")
    limit : int
        Maximum number of stocks to return if fetching data (default: 1700)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing only stocks that have non-None heating_up values
    """
    # Fetch data if not provided
    if screener_df is None:
        screener_df = get_screener_data(exchange_names, limit)
    
    # Simply filter for stocks where heating_up is not None
    heating_up_stocks = screener_df[pd.notna(screener_df['heating_up'])]
    
    if len(heating_up_stocks) == 0:
        print("\n✨ No stocks are heating up today. Market is taking a chill pill. ✨")
        print("Maybe it's time to Netflix and... diversify your portfolio? 📉😎")
    else:
        print(f"\nFound {len(heating_up_stocks)} stocks that are heating up! 🔥")
    
    return heating_up_stocks

def save_heating_up_stocks_to_csv(heating_up_stocks, filename="heating_up_stocks.csv"):
    """
    Save the heating up stocks to a CSV file.
    
    Parameters:
    -----------
    heating_up_stocks : pandas.DataFrame
        DataFrame containing heating up stocks
    filename : str
        Name of the CSV file to save (default: "heating_up_stocks.csv")
    """
    if not heating_up_stocks.empty:
        heating_up_stocks.to_csv(filename, index=False)
        print(f"Saved {len(heating_up_stocks)} heating up stocks to {filename}")
    else:
        print("No heating up stocks to save")

# Main execution
if __name__ == "__main__":
    # Get screener data
    print("Fetching screener data...")
    screener_df = get_screener_data()
    print(f"Retrieved {len(screener_df)} stocks from screener")
    print(screener_df.head())
    
    # Find heating up stocks
    heating_up_stocks = find_heating_up_stocks(screener_df)
    
    # Display heating up stocks if any were found
    if not heating_up_stocks.empty:
        print("\nHeating up stocks:")
        # Display a subset of columns for better readability
        display_columns = ['ticker', 'exchange', 'price', 'change_percent', 'volume']
        # Filter to only include columns that exist in the DataFrame
        display_columns = [col for col in display_columns if col in heating_up_stocks.columns]
        print(heating_up_stocks[display_columns].head(10))  # Show only first 10 rows
        
        # Save to CSV
        #save_heating_up_stocks_to_csv(heating_up_stocks)