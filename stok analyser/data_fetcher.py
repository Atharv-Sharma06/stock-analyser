import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period="1y"):
    """Fetch historical stock data using yfinance."""
    try:
        data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if data is None or data.empty:
            return None
        # Newer yfinance versions return MultiIndex columns (Price, Ticker) even
        # for a single ticker, which makes data['Close'] a DataFrame. Flatten it.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data.dropna(subset=['Close'])
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_current_price(ticker):
    """Get the current stock price."""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period='5d')
        if history.empty:
            return None
        return float(history['Close'].iloc[-1])
    except Exception as e:
        print(f"Error getting current price for {ticker}: {e}")
        return None

def get_stock_info(ticker):
    """Get basic stock information."""
    try:
        # Fetch .info once: each access triggers a network request and Yahoo
        # rate-limits repeated calls.
        info = yf.Ticker(ticker).info or {}
        return {
            'name': info.get('longName') or info.get('shortName') or ticker,
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
        }
    except Exception as e:
        print(f"Error getting stock info for {ticker}: {e}")
        return {}
