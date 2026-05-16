import pandas as pd
import numpy as np

def calculate_moving_average(data, window=20):
    """Calculate simple moving average."""
    return data['Close'].rolling(window=window).mean()

def calculate_exponential_moving_average(data, span=20):
    """Calculate exponential moving average."""
    return data['Close'].ewm(span=span).mean()

def calculate_returns(data):
    """Calculate daily returns."""
    return data['Close'].pct_change()

def calculate_cumulative_returns(data):
    """Calculate cumulative returns from start."""
    returns = calculate_returns(data)
    return (1 + returns).cumprod() - 1

def calculate_sharpe_ratio(data, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio.
    Assumes daily data, annualizes the metric (252 trading days).
    """
    returns = calculate_returns(data).dropna()

    annual_return = returns.mean() * 252
    annual_volatility = returns.std() * np.sqrt(252)

    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility != 0 else 0
    return sharpe_ratio

def calculate_volatility(data, window=252):
    """
    Calculate annualized volatility.
    Default window is 252 trading days (1 year).
    """
    returns = calculate_returns(data)
    daily_volatility = returns.std()
    annual_volatility = daily_volatility * np.sqrt(252)
    return annual_volatility

def calculate_max_drawdown(data):
    """Calculate maximum drawdown from peak."""
    cumulative = (1 + calculate_returns(data)).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min()

def calculate_total_return(data):
    """Calculate total return percentage."""
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    return (end_price - start_price) / start_price * 100

def get_analysis_summary(ticker, data):
    """Get comprehensive analysis summary."""
    return {
        'ticker': ticker,
        'current_price': data['Close'].iloc[-1],
        'total_return': calculate_total_return(data),
        'sharpe_ratio': calculate_sharpe_ratio(data),
        'volatility': calculate_volatility(data),
        'max_drawdown': calculate_max_drawdown(data),
        'sma_20': calculate_moving_average(data, 20).iloc[-1],
        'ema_20': calculate_exponential_moving_average(data, 20).iloc[-1],
    }
