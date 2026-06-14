import streamlit as st

from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer
from strategy.recommendation import RecommendationEngine
from ai.explanation import AIExplanation

st.set_page_config(
    page_title="AI Stock Analysis",
    layout="wide"
)

st.title("📈 AI Stock Analysis")

symbol = st.text_input(
    "Enter NSE Stock Symbol",
    value="TCS.NS"
)

if st.button("Analyze Stock"):

    with st.spinner("Analyzing Stock..."):

        df = download_stock_data(symbol)

        if df.empty:

            st.error(
                "Unable to fetch stock data."
            )

            st.stop()

        df = calculate_indicators(df)

        scorer = StockScorer()

        score_result = (
            scorer.calculate_score(
                df,
                symbol
            )
        )

        recommendation_engine = (
            RecommendationEngine()
        )

        trade_plan = (
            recommendation_engine
            .generate_trade_plan(df)
        )

        ai_engine = AIExplanation()

        ai_result = (
            ai_engine.generate(df)
        )

        latest = df.iloc[-1]

        # ===================================
        # MARKET DATA
        # ===================================

        st.subheader(
            "📊 Latest Market Data"
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "Close",
            round(
                latest["Close"],
                2
            )
        )

        c2.metric(
            "RSI",
            round(
                latest["RSI"],
                2
            )
        )

        c3.metric(
            "ADX",
            round(
                latest["ADX"],
                2
            )
        )

        c4.metric(
            "Score",
            score_result[
                "total_score"
            ]
        )

        # ===================================
        # MARKET STATUS
        # ===================================

        st.subheader(
            "🌍 Market Status"
        )

        market_status = (
            score_result[
                "market_status"
            ]
        )

        if market_status == "BULLISH":

            st.success(
                market_status
            )

        elif market_status == "SIDEWAYS":

            st.warning(
                market_status
            )

        else:

            st.error(
                market_status
            )

        # ===================================
        # MULTI TIMEFRAME
        # ===================================

        st.subheader(
            "📅 Multi Timeframe Trend"
        )

        trend = (
            score_result[
                "multi_timeframe"
            ]
        )

        if trend == "STRONG UPTREND":

            st.success(trend)

        elif trend == "MODERATE UPTREND":

            st.warning(trend)

        else:

            st.error(trend)

        # ===================================
        # PATTERN
        # ===================================

        st.subheader(
            "🕯 Candlestick Pattern"
        )

        pattern = (
            score_result[
                "pattern"
            ]
        )

        if pattern == "No Pattern":

            st.info(
                "No Major Pattern Detected"
            )

        else:

            st.success(
                pattern
            )

        # ===================================
        # RECOMMENDATION
        # ===================================

        st.subheader(
            "🤖 Recommendation"
        )

        recommendation = (
            score_result[
                "recommendation"
            ]
        )

        if recommendation == "STRONG BUY":

            st.success(
                recommendation
            )

        elif recommendation == "BUY":

            st.success(
                recommendation
            )

        elif recommendation == "HOLD":

            st.warning(
                recommendation
            )

        else:

            st.error(
                recommendation
            )

        # ===================================
        # SCORE BREAKDOWN
        # ===================================

        st.subheader(
            "📊 Score Breakdown"
        )

        st.json({

            "Trend Score":
            score_result[
                "trend_score"
            ],

            "Momentum Score":
            score_result[
                "momentum_score"
            ],

            "Volume Score":
            score_result[
                "volume_score"
            ],

            "Volatility Score":
            score_result[
                "volatility_score"
            ],

            "Strength Score":
            score_result[
                "strength_score"
            ],

            "Market Score":
            score_result[
                "market_score"
            ],

            "Pattern Score":
            score_result[
                "pattern_score"
            ],

            "Multi Timeframe Score":
            score_result[
                "multi_timeframe_score"
            ],

            "Total Score":
            score_result[
                "total_score"
            ]
        })

        # ===================================
        # TRADE PLAN
        # ===================================

        st.subheader(
            "🎯 Trade Plan"
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Entry",
            f"₹{trade_plan['entry']}"
        )

        c2.metric(
            "Stop Loss",
            f"₹{trade_plan['stop_loss']}"
        )

        c3.metric(
            "Target",
            f"₹{trade_plan['target']}"
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Risk",
            f"₹{trade_plan['risk']}"
        )

        c2.metric(
            "Reward",
            f"₹{trade_plan['reward']}"
        )

        c3.metric(
            "Risk Reward",
            trade_plan[
                "risk_reward"
            ]
        )

        rr = (
            trade_plan[
                "risk_reward"
            ]
        )

        if rr >= 2:

            st.success(
                "Excellent Risk Reward Setup ✅"
            )

        elif rr >= 1.5:

            st.warning(
                "Average Risk Reward Setup ⚠️"
            )

        else:

            st.error(
                "Poor Risk Reward Setup ❌"
            )

        # ===================================
        # AI EXPLANATION
        # ===================================

        st.subheader(
            "🧠 AI Explanation"
        )

        st.success(
            f"Signal : "
            f"{ai_result['signal']}"
        )

        st.info(
            f"Confidence : "
            f"{ai_result['confidence']}%"
        )

        for reason in (
            ai_result["reasons"]
        ):

            st.write(
                "✅",
                reason
            )

        # ===================================
        # INDICATORS
        # ===================================

        st.subheader(
            "📈 Technical Indicators"
        )

        ic1, ic2, ic3, ic4 = (
            st.columns(4)
        )

        ic1.metric(
            "EMA20",
            round(
                latest["EMA20"],
                2
            )
        )

        ic2.metric(
            "EMA50",
            round(
                latest["EMA50"],
                2
            )
        )

        ic3.metric(
            "MACD",
            round(
                latest["MACD"],
                2
            )
        )

        ic4.metric(
            "ATR",
            round(
                latest["ATR"],
                2
            )
        )

        # ===================================
        # CHART
        # ===================================

        st.subheader(
            "📉 Price Chart"
        )

        st.line_chart(
            df["Close"]
        )

        # ===================================
        # DATA
        # ===================================

        st.subheader(
            "📋 Recent Data"
        )

        st.dataframe(
            df.tail(20),
            use_container_width=True
        )