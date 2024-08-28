import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Define constants
API_KEY = "TQON2JM2Z082S1BG"
BASE_URL = "https://www.alphavantage.co/query"

# List of Indian stocks to track (symbols with exchange suffixes)
INDIAN_STOCKS = ["RELIANCE", "TCS.BSE", "WIPRO.BSE", "LTIM.BSE", "MARUTI.BSE"]


# Function to get daily stock data
def get_stock_data(symbol, api_key):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact",
        "datatype": "json",
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data


# Function to analyze stock data
def analyze_stock_data(symbol):
    data = get_stock_data(symbol, API_KEY)
    try:
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df = df.sort_index(ascending=False).head(5)  # Last 5 days
        df["Average"] = df[["1. open", "2. high", "3. low", "4. close"]].mean(axis=1)
        avg_last_5_days = df["Average"].mean()
        avg_change = avg_last_5_days - df["Average"].iloc[-1]

        # Determine if the stock is up or down
        trend = "up" if avg_change > 0 else "down"
        return f"{symbol}: Average Price Change is {trend}. Avg: {avg_last_5_days:.2f}, Latest: {df['Average'].iloc[-1]:.2f}"
    except KeyError:
        return f"Error fetching data for {symbol}. Please check the symbol or API key."


# Function to display stock data
def display_stock_data():
    output_text.delete(1.0, tk.END)
    for stock in INDIAN_STOCKS:
        result = analyze_stock_data(stock)
        output_text.insert(tk.END, f"{result}\n")


# Create the main window
root = tk.Tk()
root.title("Stock Market Advisor - Indian Stocks")

# Create and place widgets
tk.Label(root, text="Stock Market Advisor - Last 5 Days (Indian Stocks)").grid(
    row=0, column=0, padx=10, pady=10
)

btn_fetch = tk.Button(root, text="Fetch and Analyze Data", command=display_stock_data)
btn_fetch.grid(row=1, column=0, padx=10, pady=10)

output_text = tk.Text(root, height=15, width=80)
output_text.grid(row=2, column=0, padx=10, pady=10)

# Run the application
root.mainloop()
