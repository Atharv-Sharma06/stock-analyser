# Stock Analyzer

A Python-powered equity analyzer for streamlined investment research. Pulls live stock data, computes technical indicators, and calculates key risk metrics.

## Features

- **Live Data Fetching**: Real-time stock data via yfinance
- **Technical Analysis**: 
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Daily returns & cumulative returns
- **Risk Metrics**:
  - Sharpe Ratio (risk-adjusted returns)
  - Volatility (annualized)
  - Maximum Drawdown
- **Visualizations**:
  - Price trends with moving averages
  - Returns distribution & cumulative performance
  - Rolling volatility analysis
  - Drawdown chart

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then navigate to the local Streamlit server (usually `http://localhost:8501`) and enter a stock ticker to analyze.

## Modules

- **data_fetcher.py**: Fetch stock data and company info
- **analyzer.py**: Calculate technical indicators and metrics
- **visualizations.py**: Generate charts and plots
- **app.py**: Interactive Streamlit interface

## Example Tickers

AAPL, MSFT, GOOGL, TSLA, AMZN, etc.
