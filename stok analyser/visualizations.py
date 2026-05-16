import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from analyzer import (
    calculate_moving_average,
    calculate_exponential_moving_average,
    calculate_returns,
    calculate_cumulative_returns,
    calculate_max_drawdown
)

def plot_price_trend(data, ticker, show_ma=True):
    """Plot stock price trend with moving averages."""
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(data.index, data['Close'], label='Close Price', linewidth=2, color='blue')

    if show_ma:
        sma_20 = calculate_moving_average(data, 20)
        ema_20 = calculate_exponential_moving_average(data, 20)
        ax.plot(data.index, sma_20, label='SMA 20', linewidth=1.5, alpha=0.7, color='orange')
        ax.plot(data.index, ema_20, label='EMA 20', linewidth=1.5, alpha=0.7, color='red')

    ax.set_title(f'{ticker} - Price Trend', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

def plot_returns(data, ticker):
    """Plot daily returns distribution."""
    returns = calculate_returns(data).dropna()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.hist(returns, bins=50, edgecolor='black', alpha=0.7, color='skyblue')
    ax1.set_title(f'{ticker} - Daily Returns Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Daily Return', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.grid(True, alpha=0.3)

    cumulative = calculate_cumulative_returns(data)
    ax2.plot(data.index, cumulative * 100, linewidth=2, color='green')
    ax2.fill_between(data.index, cumulative * 100, alpha=0.3, color='green')
    ax2.set_title(f'{ticker} - Cumulative Returns', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=11)
    ax2.set_ylabel('Cumulative Return (%)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()
    return fig

def plot_volatility(data, ticker, window=30):
    """Plot rolling volatility."""
    returns = calculate_returns(data)
    rolling_volatility = returns.rolling(window=window).std() * (252 ** 0.5)

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(data.index, rolling_volatility, linewidth=2, color='purple')
    ax.fill_between(data.index, rolling_volatility, alpha=0.3, color='purple')
    ax.set_title(f'{ticker} - Rolling Volatility (Annualized, {window}-day window)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Volatility', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

def plot_drawdown(data, ticker):
    """Plot maximum drawdown over time."""
    cumulative = (1 + calculate_returns(data)).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(data.index, drawdown, 0, alpha=0.5, color='red', label='Drawdown')
    ax.plot(data.index, drawdown, linewidth=1.5, color='darkred')
    ax.set_title(f'{ticker} - Drawdown from Peak', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Drawdown (%)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
