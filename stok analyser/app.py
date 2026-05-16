import streamlit as st
import pandas as pd
from data_fetcher import fetch_stock_data, get_current_price, get_stock_info
from analyzer import (
    get_analysis_summary,
    calculate_moving_average,
    calculate_volatility,
)
from visualizations import (
    plot_price_trend,
    plot_returns,
    plot_volatility,
    plot_drawdown,
)

st.set_page_config(page_title="Stock Analyzer", layout="wide")

st.title("📈 Stock Analyzer")
st.markdown("Live stock data analysis, technical indicators, and risk metrics")

col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, GOOGL)", value="AAPL").upper()
with col2:
    period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])

if ticker:
    try:
        data = fetch_stock_data(ticker, period=period)

        if data is not None and not data.empty:
            info = get_stock_info(ticker)
            summary = get_analysis_summary(ticker, data)

            st.markdown(f"## {info.get('name', ticker)} ({ticker})")

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Current Price", f"${summary['current_price']:.2f}")
            with col2:
                st.metric("Total Return", f"{summary['total_return']:.2f}%")
            with col3:
                st.metric("Sharpe Ratio", f"{summary['sharpe_ratio']:.2f}")
            with col4:
                st.metric("Volatility", f"{summary['volatility']:.2%}")
            with col5:
                st.metric("Max Drawdown", f"{summary['max_drawdown']:.2%}")

            st.divider()

            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["📊 Price Trend", "📉 Returns", "📈 Volatility", "⬇️ Drawdown", "📋 Details"]
            )

            with tab1:
                fig = plot_price_trend(data, ticker, show_ma=True)
                st.pyplot(fig)

            with tab2:
                fig = plot_returns(data, ticker)
                st.pyplot(fig)

            with tab3:
                fig = plot_volatility(data, ticker)
                st.pyplot(fig)

            with tab4:
                fig = plot_drawdown(data, ticker)
                st.pyplot(fig)

            with tab5:
                st.subheader("Stock Information")
                info_cols = st.columns(3)
                with info_cols[0]:
                    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                with info_cols[1]:
                    st.write(f"**52-Week High:** ${info.get('52_week_high', 'N/A')}")
                    st.write(f"**52-Week Low:** ${info.get('52_week_low', 'N/A')}")

                st.subheader("Moving Averages")
                sma_20 = calculate_moving_average(data, 20).iloc[-1]
                st.write(f"**SMA 20:** ${sma_20:.2f}")

                st.subheader("Raw Data")
                st.dataframe(data.tail(10))

        else:
            st.error(f"Could not fetch data for {ticker}. Please check the ticker symbol.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Enter a stock ticker to begin analysis.")
