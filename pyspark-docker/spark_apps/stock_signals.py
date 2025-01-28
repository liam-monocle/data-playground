import yfinance as yf
import pandas as pd

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    print(f"Fetching data for {ticker}...")
    return yf.download(ticker, start=start_date, end=end_date)

# Function to calculate trading signals
def generate_trading_signals(data, moving_avg_period=20):
    # Ensure the index is a DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    # Sort the index to ensure proper time ordering
    data = data.sort_index()

    # Add moving averages to the data
    data["Moving Average"] = data["Close"].rolling(window=moving_avg_period, min_periods=1).mean()

    # Identify previous highs and lows
    data["Previous High"] = data["High"].shift(1)  # Shift highs forward by one day
    data["Previous Low"] = data["Low"].shift(1)    # Shift lows forward by one day

    # print(data.index)
    print("Close index")
    print(data["Close"].index)
    print("Previous High Index")
    print(data["Previous High"].index)
    print("Moving Average")
    print(data["Moving Average"].index)
 
     # Align columns before comparisons
    data["Close_Aligned"], data["Previous_High_Aligned"] = data["Close"].align(data["Previous High"], axis=0, copy=False)
    data["Close_Aligned_Low"], data["Previous_Low_Aligned"] = data["Close"].align(data["Previous Low"], axis=0, copy=False)

    # Generate warnings
    data["Above High"] = data["Close_Aligned"] > data["Previous_High_Aligned"]
    data["Below Low"] = data["Close_Aligned_Low"] < data["Previous_Low_Aligned"]

    # Drop temporary aligned columns
    data = data.drop(columns=["Close_Aligned", "Previous_High_Aligned", "Close_Aligned_Low", "Previous_Low_Aligned"])

    # Return the updated DataFrame
    return data

# Function to display alerts and dates of breaches
def display_alerts_with_dates(data):
    alerts = []
    # Ensure 'Above High' and 'Below Low' columns are boolean
    data["Above High"] = data["Above High"].fillna(False).astype(bool)
    data["Below Low"] = data["Below Low"].fillna(False).astype(bool)
    
    for index, row in data.iterrows():
        if row["Above High"].item() if isinstance(row["Above High"], pd.Series) else row["Above High"]:
            alerts.append({
                'Date': index.date(),
                'Event': 'Broke Above High',
                'Previous Value': row['Previous High'].name,
                'Close': row['Close'].name
            })
        if row["Below Low"].item() if isinstance(row["Below Low"], pd.Series) else row["Below Low"]:
            alerts.append({
                'Date': index.date(),
                'Event': 'Broke Below Low',
                'Previous Value': row['Previous Low'].name,
                'Close': row['Close'].name
            })
    return alerts

# Main script
if __name__ == "__main__":
# Define the ticker symbol and the date range
    ticker = "TSLA"
    start_date = "2024-01-01"  # 2 years ago from today
    end_date = "2025-01-01"    # Adjust the end date as needed

    # # Download Stock data
    # stock_data = yf.download(ticker, start=start_date, end=end_date)
    # output_csv_file = "stock_data.csv"

    # stock_data.to_csv(output_csv_file)
    # # Save the data as a Parquet file
    # output_parquet_file = "stock_data.parquet"
    # stock_data.to_parquet(output_parquet_file)

    # print(f"stock data saved to parquet {output_parquet_file}")
    # print(f"stock data saved to csv {output_csv_file}")

    # Fetch stock data
    stock_data = fetch_stock_data(ticker, start_date, end_date)

    # Generate trading signals
    stock_data = generate_trading_signals(stock_data)

    # Display alerts
    # Fetch stock data
    stock_data = fetch_stock_data(ticker, start_date, end_date)

    # Generate trading signals
    stock_data = generate_trading_signals(stock_data)

    # Display alerts with dates
    alerts = display_alerts_with_dates(stock_data)
    
    # Print alerts with dates
    above_previous_high = 0
    below_previous_Low = 0
    for alert in alerts:
        above_previous_high += 1
        
        if alert['Event'] == 'Broke Above High':

            print(f"On {alert['Date']}: Price broke ABOVE previous high of {alert['Previous Value']}. Current Close: {alert['Close']}")
        elif alert['Event'] == 'Broke Below Low':
            below_previous_Low += 1

            print(f"On {alert['Date']}: Price broke BELOW previous low of {alert['Previous Value']}. Current Close: {alert['Close']}")

    print(f"above_previous_high Count: {above_previous_high}")
    print(f"below_previous_Low Count: {below_previous_Low}")
    # Save data with signals to a CSV file
    # output_file = "tesla_trading_signals.csv"
    # stock_data.to_csv(output_file)
    # print(f"\nTrading signals saved to {output_file}")
