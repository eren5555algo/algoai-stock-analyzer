
import streamlit as st
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt

st.set_page_config(page_title="AlgoAi - Stock Analysis Tool")
st.title("AlgoAi - AI Powered Stock Analysis")

# Input
symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA):", "AAPL")

# Fetch data
if symbol:
    df = yf.download(symbol, period="6mo", interval="1d")
    if df.empty:
        st.error("Failed to fetch data. Please check the symbol.")
    else:
        st.success(f"Data loaded for {symbol}")

        # Technical Indicators
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['RSI_14'] = ta.rsi(df['Close'], length=14)
        macd = ta.macd(df['Close'])
        df = df.join(macd)

        # Fibonacci Retracement (basic version)
        max_price = df['Close'].max()
        min_price = df['Close'].min()
        diff = max_price - min_price
        levels = [max_price - diff * ratio for ratio in [0.236, 0.382, 0.5, 0.618, 0.786]]

        # Plot Price and SMA
        st.subheader("Price Chart with SMA")
        fig, ax = plt.subplots()
        ax.plot(df.index, df['Close'], label='Close Price')
        ax.plot(df.index, df['SMA_20'], label='SMA 20', linestyle='--')
        for level in levels:
            ax.axhline(level, linestyle='--', color='grey', alpha=0.5)
        ax.set_title(f"{symbol} Price & Fibonacci Levels")
        ax.legend()
        st.pyplot(fig)

        # RSI
        st.subheader("RSI")
        st.line_chart(df['RSI_14'])

        # MACD
        st.subheader("MACD")
        st.line_chart(df[['MACD_12_26_9', 'MACDs_12_26_9']])

        # Summary (mock placeholder for AI)
        st.subheader("Summary")
        trend = "upward" if df['SMA_20'].iloc[-1] > df['SMA_20'].iloc[-20] else "downward"
        st.info(f"The stock appears to be in a {trend} trend. RSI is at {df['RSI_14'].iloc[-1]:.2f}.")
