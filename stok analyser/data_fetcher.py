import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period="1y"):
    """Fetch historical stock data using yfinance."""
    try:
        data = yf.download(ticker, period=period, progress=False)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_current_price(ticker):
    """Get the current stock price."""
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get('currentPrice') or stock.history(period='1d')['Close'].iloc[-1]
        return current_price
    except Exception as e:
        print(f"Error getting current price for {ticker}: {e}")
        return None

def get_stock_info(ticker):
    """Get basic stock information."""
    try:
        stock = yf.Ticker(ticker)
        return {
            'name': stock.info.get('longName', ticker),
            'sector': stock.info.get('sector', 'N/A'),
            'industry': stock.info.get('industry', 'N/A'),
            '52_week_high': stock.info.get('fiftyTwoWeekHigh', 'N/A'),
            '52_week_low': stock.info.get('fiftyTwoWeekLow', 'N/A'),
        }
    except Exception as e:
        print(f"Error getting stock info for {ticker}: {e}")
        return {}
