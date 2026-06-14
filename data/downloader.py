import pandas as pd
import streamlit as st
import yfinance as yf

from utils.logger import log_info, log_error


@st.cache_data(ttl=300)
def download_stock_data(
    symbol: str,
    period: str = "1y",
    interval: str = "1d",
):
    """
    Download stock data with caching and return
    a clean DataFrame.
    """

    try:

        log_info(
            f"Downloading {symbol} | Period={period} | Interval={interval}"
        )

        df = yf.download(
            tickers=symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
        )

        if df.empty:
            log_error(f"No data returned for {symbol}")
            return pd.DataFrame()

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Remove missing values
        df = df.dropna()

        return df

    except Exception as e:

        log_error(str(e))

        return pd.DataFrame()