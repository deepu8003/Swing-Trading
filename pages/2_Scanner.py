import streamlit as st
import pandas as pd

from data.nifty50 import NIFTY50
from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer
from strategy.recommendation import RecommendationEngine

st.title("🚀 Swing Trading Scanner")

if st.button("Scan NIFTY 50"):

    scorer = StockScorer()
    planner = RecommendationEngine()

    results = []

    progress = st.progress(0)

    total = len(NIFTY50)

    for idx, symbol in enumerate(NIFTY50):

        try:

            df = download_stock_data(symbol)

            if df.empty:
                continue

            df = calculate_indicators(df)

            score = scorer.calculate_score(df)

            trade = planner.generate_trade_plan(df)

            results.append({
                "Symbol": symbol,
                "Score": score["total_score"],
                "Signal": score["recommendation"],
                "Entry": trade["entry"],
                "Stop Loss": trade["stop_loss"],
                "Target": trade["target"],
                "RR": trade["risk_reward"]
            })

        except Exception:
            pass

        progress.progress((idx + 1) / total)

    results = sorted(
        results,
        key=lambda x: x["Score"],
        reverse=True
    )

    df_result = pd.DataFrame(results)

    st.subheader("Top Swing Opportunities")

    st.dataframe(
        df_result,
        use_container_width=True
    )

    top5 = df_result.head(5)

    st.subheader("🔥 Top 5 Stocks")

    st.dataframe(
        top5,
        use_container_width=True
    )