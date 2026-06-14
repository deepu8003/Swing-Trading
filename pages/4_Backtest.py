import streamlit as st

from data.downloader import download_stock_data
from backtest.engine import BacktestEngine

st.title("🧪 Backtesting")

symbol = st.text_input(
    "Symbol",
    value="TCS.NS"
)

if st.button("Run Backtest"):

    df = download_stock_data(
        symbol,
        period="2y"
    )

    engine = BacktestEngine()

    result = engine.run_backtest(df)

    st.write(result)