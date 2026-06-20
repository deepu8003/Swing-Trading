import streamlit as st

from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer
from strategy.recommendation import RecommendationEngine
from ai.explanation import AIExplanation


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Stock Analysis",
    layout="wide"
)

st.title("📈 AI Stock Analysis")

st.caption(
    "Professional swing-trading analysis for NSE stocks. "
    "Scores are computed from trend, momentum, volume, "
    "breakout strength, and risk — weighted into a single "
    "0-100 composite score."
)

# ======================================================
# INPUT
# ======================================================

symbol = st.text_input(
    "Enter NSE Stock Symbol",
    value="TCS.NS"
)

if not st.button("Analyze Stock"):
    st.stop()

# ======================================================
# DATA & INDICATORS
# ======================================================

with st.spinner("Fetching data and calculating indicators…"):

    df = download_stock_data(symbol)

    if df.empty:
        st.error(
            "Unable to fetch stock data. "
            "Check the symbol and try again."
        )
        st.stop()

    df = calculate_indicators(df)

# ======================================================
# SCORING
# ======================================================

with st.spinner("Running scoring engine…"):

    scorer       = StockScorer()
    score_result = scorer.calculate_score(df, symbol)

    recommendation_engine = RecommendationEngine()
    trade_plan            = recommendation_engine.generate_trade_plan(df)

    ai_engine  = AIExplanation()
    ai_result  = ai_engine.generate(df)

latest = df.iloc[-1]

# ======================================================
# HEADER SNAPSHOT
# ======================================================

st.subheader("📊 Snapshot")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Close Price",
    f"₹{round(latest['Close'], 2)}"
)
c2.metric(
    "Final Score",
    f"{score_result['total_score']} / 100"
)
c3.metric(
    "Classification",
    score_result["classification"]
)
c4.metric(
    "Success Probability",
    f"{score_result['success_probability']}%"
)
c5.metric(
    "Market",
    score_result["market_status"]
)

st.divider()

# ======================================================
# RECOMMENDATION BANNER
# ======================================================

recommendation = score_result["recommendation"]

_REC_FN = {
    "STRONG BUY": st.success,
    "BUY":        st.success,
    "HOLD":       st.warning,
    "SELL":       st.error,
}
_REC_FN.get(recommendation, st.info)(
    f"🤖 Recommendation: **{recommendation}**  |  "
    f"Classification: **{score_result['classification']}**  |  "
    f"Success Probability: **{score_result['success_probability']}%**"
)

st.divider()

# ======================================================
# TREND ANALYSIS
# ======================================================

st.subheader("📐 Trend Analysis")

trend_score   = score_result["trend_score"]
trend_label   = score_result["trend_label"]
trend_details = score_result["trend_details"]

col_left, col_right = st.columns([1, 2])

with col_left:

    _trend_color = {
        "Strong Bullish": "success",
        "Bullish":        "success",
        "Neutral":        "warning",
        "Bearish":        "error",
        "Strong Bearish": "error",
    }.get(trend_label, "info")

    getattr(st, _trend_color)(
        f"**{trend_label}**  —  Score: {trend_score}/100"
    )

    st.progress(trend_score / 100)

    st.caption(
        "Trend score measures whether the stock is moving "
        "in an upward direction using multiple moving averages."
    )

with col_right:

    t1, t2, t3 = st.columns(3)

    t1.metric(
        "EMA 20",
        round(float(latest["EMA20"]), 2)
    )
    t2.metric(
        "EMA 50",
        round(float(latest["EMA50"]), 2)
    )
    t3.metric(
        "SMA 200",
        round(float(latest.get("SMA200", 0)), 2)
    )

    flags = []
    if trend_details.get("ema20_above_ema50"):
        flags.append("✅ EMA20 > EMA50 (Short-term uptrend)")
    else:
        flags.append("❌ EMA20 < EMA50 (Short-term downtrend)")

    if trend_details.get("above_sma200"):
        flags.append("✅ Price above SMA200 (Long-term uptrend)")
    else:
        flags.append("❌ Price below SMA200 (Long-term downtrend)")

    if trend_details.get("golden_cross"):
        flags.append("🌟 Golden Cross detected (Strong bullish signal)")

    if trend_details.get("death_cross"):
        flags.append("💀 Death Cross detected (Strong bearish signal)")

    for f in flags:
        st.write(f)

st.divider()

# ======================================================
# MOMENTUM ANALYSIS
# ======================================================

st.subheader("⚡ Momentum Analysis")

momentum_score   = score_result["momentum_score"]
momentum_label   = score_result["momentum_label"]
momentum_details = score_result["momentum_details"]

col_left, col_right = st.columns([1, 2])

with col_left:

    _mom_color = (
        "success" if momentum_score >= 60
        else "warning" if momentum_score >= 35
        else "error"
    )
    getattr(st, _mom_color)(
        f"**{momentum_label}**  —  Score: {momentum_score}/100"
    )
    st.progress(momentum_score / 100)

    st.caption(
        "Momentum shows how fast and strongly the "
        "stock is moving. High momentum = strong buying pressure."
    )

with col_right:

    m1, m2, m3 = st.columns(3)

    m1.metric("RSI (14)", momentum_details.get("rsi", "-"))
    m2.metric("MACD Hist", momentum_details.get("macd_hist", "-"))
    m3.metric("ADX", momentum_details.get("adx", "-"))

    # RSI zone explanation
    rsi_zone = momentum_details.get("rsi_zone", "")
    rsi_val  = momentum_details.get("rsi", 50)

    _rsi_map = {
        "Bullish":        ("✅", "RSI in bullish zone (55-70) — good momentum"),
        "Mildly Bullish": ("🟡", "RSI just crossed 50 — momentum building"),
        "Overbought":     ("⚠️", "RSI above 70 — stock may be overbought"),
        "Oversold":       ("🔄", "RSI below 30 — possible bounce opportunity"),
        "Neutral":        ("➖", "RSI near 50 — no clear momentum"),
        "Weak":           ("❌", "RSI below 45 — weak or falling momentum"),
    }
    emoji, desc = _rsi_map.get(rsi_zone, ("➖", rsi_zone))
    st.write(f"{emoji} {desc}")

    if momentum_details.get("macd_above_signal"):
        st.write("✅ MACD above signal line — bullish crossover")
    else:
        st.write("❌ MACD below signal line — bearish")

    if momentum_details.get("macd_hist_expanding"):
        st.write("✅ MACD histogram expanding — momentum accelerating")
    else:
        st.write("❌ MACD histogram shrinking — momentum fading")

    st.write(
        f"📊 ADX Strength: "
        f"**{momentum_details.get('adx_strength', 'Unknown')}**"
    )

st.divider()

# ======================================================
# VOLUME ANALYSIS
# ======================================================

st.subheader("📦 Volume Analysis")

volume_score   = score_result["volume_score"]
volume_label   = score_result["volume_label"]
volume_details = score_result["volume_details"]

col_left, col_right = st.columns([1, 2])

with col_left:

    _vol_color = (
        "success" if volume_score >= 60
        else "warning" if volume_score >= 30
        else "error"
    )
    getattr(st, _vol_color)(
        f"**{volume_label}**  —  Score: {volume_score}/100"
    )
    st.progress(volume_score / 100)

    st.caption(
        "Volume confirms price moves. "
        "High volume on a rising price = strong buyer conviction."
    )

with col_right:

    v1, v2 = st.columns(2)

    rel_vol = volume_details.get("relative_volume", 1.0)
    v1.metric(
        "Relative Volume",
        f"{rel_vol}x"
    )
    v2.metric(
        "Above-Avg Days (5)",
        volume_details.get("above_avg_vol_days", "-")
    )

    st.write(
        f"📊 Volume Tier: **{volume_details.get('volume_tier', '-')}**"
    )

    if volume_details.get("breakout_volume_confirmed"):
        st.success(
            "✅ Breakout volume confirmed — "
            "price rising on above-average volume"
        )
    else:
        st.info(
            "ℹ️ No breakout volume confirmation yet"
        )

    if volume_details.get("obv_rising"):
        st.write(
            "✅ OBV rising — institutional accumulation detected"
        )
    else:
        st.write(
            "❌ OBV falling — possible distribution"
        )

st.divider()

# ======================================================
# RISK ANALYSIS
# ======================================================

st.subheader("🛡️ Risk Analysis")

risk_score   = score_result["risk_score"]
risk_label   = score_result["risk_label"]
risk_details = score_result["risk_details"]

col_left, col_right = st.columns([1, 2])

with col_left:

    _risk_color = {
        "Low Risk":    "success",
        "Medium Risk": "warning",
        "High Risk":   "error",
    }.get(risk_label, "info")

    getattr(st, _risk_color)(
        f"**{risk_label}**  —  Risk Score: {risk_score}/100"
    )
    st.progress(risk_score / 100)

    st.caption(
        "Risk score is higher when the stock is "
        "less volatile and in a stable, controlled move. "
        "Higher score = safer to trade."
    )

with col_right:

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "ATR%",
        f"{risk_details.get('atr_pct', '-')}%"
    )
    r2.metric("+DI", risk_details.get("di_pos", "-"))
    r3.metric("−DI", risk_details.get("di_neg", "-"))

    st.write(
        f"📊 Volatility: "
        f"**{risk_details.get('volatility_tier', '-')}**"
    )

    if risk_details.get("above_bb_middle"):
        st.write(
            "✅ Price above Bollinger mid-band — "
            "positive bias"
        )
    else:
        st.write(
            "❌ Price below Bollinger mid-band — "
            "weak bias"
        )

    if risk_details.get("not_bb_extended"):
        st.write(
            "✅ Price not extended — "
            "room to move up"
        )
    else:
        st.write(
            "⚠️ Price near upper band — "
            "possible short-term pullback risk"
        )

    if risk_details.get("bullish_di"):
        st.write(
            "✅ +DI > −DI — "
            "buyers in control"
        )
    else:
        st.write(
            "❌ −DI > +DI — "
            "sellers in control"
        )

st.divider()

# ======================================================
# SUPPORT & RESISTANCE
# ======================================================

st.subheader("🏹 Support & Resistance")

breakout_score   = score_result["breakout_score"]
breakout_label   = score_result["breakout_label"]
breakout_details = score_result["breakout_details"]

close_price  = float(latest["Close"])
support      = breakout_details.get("support",    close_price * 0.95)
resistance   = breakout_details.get("resistance", close_price * 1.05)

col_left, col_right = st.columns([1, 2])

with col_left:

    _brk_color = (
        "success" if breakout_score >= 60
        else "warning" if breakout_score >= 30
        else "info"
    )
    getattr(st, _brk_color)(
        f"**{breakout_label}**  —  Score: {breakout_score}/100"
    )
    st.progress(breakout_score / 100)

    st.caption(
        "Breakout detection identifies when a stock "
        "pushes above key resistance with strong volume — "
        "often the best entry signal."
    )

with col_right:

    b1, b2, b3 = st.columns(3)

    b1.metric("Support",    f"₹{support}")
    b2.metric("Close",      f"₹{round(close_price, 2)}")
    b3.metric("Resistance", f"₹{resistance}")

    dist_support    = round(
        ((close_price - support) / support) * 100, 2
    )
    dist_resistance = round(
        ((resistance - close_price) / close_price) * 100, 2
    )

    st.write(
        f"📍 Price is **{dist_support}%** above support  |  "
        f"**{dist_resistance}%** below resistance"
    )

    if breakout_details.get("price_above_resistance"):
        st.success(
            "🚀 Price breaking above resistance — "
            "potential breakout in progress!"
        )
    elif breakout_details.get("near_support"):
        st.warning(
            "⚠️ Price near support — watch for breakdown or bounce"
        )
    else:
        st.info(
            "ℹ️ Price trading between support and resistance"
        )

    if breakout_details.get("bb_squeeze_breakout"):
        st.success(
            "💥 Bollinger Band squeeze breakout detected — "
            "volatility expansion after consolidation"
        )

st.divider()

# ======================================================
# TRADE SETUP
# ======================================================

st.subheader("🎯 Trade Setup")

trade_setup = score_result.get("trade_setup", {})

# Fall back to RecommendationEngine output if scorer
# trade_setup is empty (keeps backward compatibility)
if not trade_setup:
    trade_setup = {
        "entry":           trade_plan.get("entry", 0),
        "stop_loss":       trade_plan.get("stop_loss", 0),
        "target":          trade_plan.get("target", 0),
        "risk":            trade_plan.get("risk", 0),
        "reward":          trade_plan.get("reward", 0),
        "risk_reward":     trade_plan.get("risk_reward", 0),
        "expected_return": 0,
    }

ts1, ts2, ts3 = st.columns(3)

ts1.metric("Entry Price",   f"₹{trade_setup.get('entry', '-')}")
ts2.metric("Stop Loss",     f"₹{trade_setup.get('stop_loss', '-')}")
ts3.metric("Target Price",  f"₹{trade_setup.get('target', '-')}")

ts4, ts5, ts6 = st.columns(3)

ts4.metric("Risk (₹)",         f"₹{trade_setup.get('risk', '-')}")
ts5.metric("Reward (₹)",       f"₹{trade_setup.get('reward', '-')}")
ts6.metric("Expected Return",  f"{trade_setup.get('expected_return', '-')}%")

rr = trade_setup.get("risk_reward", 0)

st.metric("Risk : Reward", f"1 : {rr}")

if rr >= 2:
    st.success("✅ Excellent Risk-Reward Setup (1:2 or better)")
elif rr >= 1.5:
    st.warning("⚠️ Average Risk-Reward Setup (1:1.5)")
else:
    st.error("❌ Poor Risk-Reward Setup — consider waiting")

st.divider()

# ======================================================
# MULTI-TIMEFRAME & PATTERN
# ======================================================

st.subheader("📅 Additional Signals")

sig1, sig2 = st.columns(2)

with sig1:

    st.markdown("**Multi-Timeframe Trend**")

    mtf = score_result["multi_timeframe"]

    if "UPTREND" in mtf:
        st.success(mtf)
    elif "DOWNTREND" in mtf:
        st.error(mtf)
    else:
        st.warning(mtf)

with sig2:

    st.markdown("**Candlestick Pattern**")

    pattern = score_result["pattern"]

    if pattern == "No Pattern":
        st.info("No Major Pattern Detected")
    else:
        st.success(pattern)

st.divider()

# ======================================================
# MARKET STATUS
# ======================================================

st.subheader("🌍 Market Status (NIFTY)")

market_status = score_result["market_status"]

_market_fn = {
    "BULLISH":  st.success,
    "SIDEWAYS": st.warning,
    "BEARISH":  st.error,
    "UNKNOWN":  st.info,
}
_market_fn.get(market_status, st.info)(
    f"NIFTY Market Condition: **{market_status}**"
)

if market_status == "BEARISH":
    st.warning(
        "⚠️ Market is bearish. Even good stocks may "
        "struggle. Reduce position size and tighten "
        "your stop loss."
    )
elif market_status == "SIDEWAYS":
    st.info(
        "ℹ️ Market is sideways. Trade only high-scoring "
        "setups and keep targets conservative."
    )

st.divider()

# ======================================================
# AI EXPLANATION
# ======================================================

st.subheader("🧠 AI Explanation")

st.success(f"Signal: {ai_result['signal']}")
st.info(f"Confidence: {ai_result['confidence']}%")

for reason in ai_result["reasons"]:
    st.write("✅", reason)

st.divider()

# ======================================================
# SCORE BREAKDOWN
# ======================================================

st.subheader("📊 Score Breakdown")

st.caption(
    "Each component is scored 0-100 and then weighted "
    "into the final composite. "
    "Trend 35% · Momentum 25% · Volume 20% · "
    "Breakout 10% · Risk 10%"
)

sb1, sb2, sb3, sb4, sb5 = st.columns(5)

sb1.metric("Trend",    f"{score_result['trend_score']}/100")
sb2.metric("Momentum", f"{score_result['momentum_score']}/100")
sb3.metric("Volume",   f"{score_result['volume_score']}/100")
sb4.metric("Breakout", f"{score_result['breakout_score']}/100")
sb5.metric("Risk",     f"{score_result['risk_score']}/100")

# Visual progress bars for all 5 components
components = {
    "Trend":    score_result["trend_score"],
    "Momentum": score_result["momentum_score"],
    "Volume":   score_result["volume_score"],
    "Breakout": score_result["breakout_score"],
    "Risk":     score_result["risk_score"],
}
for name, val in components.items():
    st.progress(
        val / 100,
        text=f"{name}: {val}/100"
    )

st.divider()

# ======================================================
# TECHNICAL INDICATORS SNAPSHOT
# ======================================================

st.subheader("📈 Technical Indicators")

ic1, ic2, ic3, ic4 = st.columns(4)

ic1.metric("EMA 20",  round(float(latest["EMA20"]), 2))
ic2.metric("EMA 50",  round(float(latest["EMA50"]), 2))
ic3.metric("RSI",     round(float(latest["RSI"]),   2))
ic4.metric("ADX",     round(float(latest["ADX"]),   2))

ic5, ic6, ic7, ic8 = st.columns(4)

ic5.metric("MACD",    round(float(latest["MACD"]),      4))
ic6.metric("ATR",     round(float(latest["ATR"]),       2))
ic7.metric("SMA 50",  round(float(latest.get("SMA50",  0)), 2))
ic8.metric("SMA 200", round(float(latest.get("SMA200", 0)), 2))

# ======================================================
# PRICE CHART
# ======================================================

st.subheader("📉 Price Chart")

st.line_chart(df["Close"])

# ======================================================
# RECENT DATA
# ======================================================

st.subheader("📋 Recent Data (Last 20 Bars)")

display_cols = [
    c for c in [
        "Open", "High", "Low", "Close", "Volume",
        "EMA20", "EMA50", "SMA50", "SMA200",
        "RSI", "MACD", "ADX", "ATR_PCT", "REL_VOL",
        "BB_UPPER", "BB_LOWER"
    ]
    if c in df.columns
]

st.dataframe(
    df[display_cols].tail(20).round(2),
    use_container_width=True
)









# import streamlit as st

# from data.downloader import download_stock_data
# from indicators.technical import calculate_indicators
# from scoring.stock_score import StockScorer
# from strategy.recommendation import RecommendationEngine
# from ai.explanation import AIExplanation

# st.set_page_config(
#     page_title="AI Stock Analysis",
#     layout="wide"
# )

# st.title("📈 AI Stock Analysis")

# symbol = st.text_input(
#     "Enter NSE Stock Symbol",
#     value="TCS.NS"
# )

# if st.button("Analyze Stock"):

#     with st.spinner("Analyzing Stock..."):

#         df = download_stock_data(symbol)

#         if df.empty:

#             st.error(
#                 "Unable to fetch stock data."
#             )

#             st.stop()

#         df = calculate_indicators(df)

#         scorer = StockScorer()

#         score_result = (
#             scorer.calculate_score(
#                 df,
#                 symbol
#             )
#         )

#         recommendation_engine = (
#             RecommendationEngine()
#         )

#         trade_plan = (
#             recommendation_engine
#             .generate_trade_plan(df)
#         )

#         ai_engine = AIExplanation()

#         ai_result = (
#             ai_engine.generate(df)
#         )

#         latest = df.iloc[-1]

#         # ===================================
#         # MARKET DATA
#         # ===================================

#         st.subheader(
#             "📊 Latest Market Data"
#         )

#         c1, c2, c3, c4 = (
#             st.columns(4)
#         )

#         c1.metric(
#             "Close",
#             round(
#                 latest["Close"],
#                 2
#             )
#         )

#         c2.metric(
#             "RSI",
#             round(
#                 latest["RSI"],
#                 2
#             )
#         )

#         c3.metric(
#             "ADX",
#             round(
#                 latest["ADX"],
#                 2
#             )
#         )

#         c4.metric(
#             "Score",
#             score_result[
#                 "total_score"
#             ]
#         )

#         # ===================================
#         # MARKET STATUS
#         # ===================================

#         st.subheader(
#             "🌍 Market Status"
#         )

#         market_status = (
#             score_result[
#                 "market_status"
#             ]
#         )

#         if market_status == "BULLISH":

#             st.success(
#                 market_status
#             )

#         elif market_status == "SIDEWAYS":

#             st.warning(
#                 market_status
#             )

#         else:

#             st.error(
#                 market_status
#             )

#         # ===================================
#         # MULTI TIMEFRAME
#         # ===================================

#         st.subheader(
#             "📅 Multi Timeframe Trend"
#         )

#         trend = (
#             score_result[
#                 "multi_timeframe"
#             ]
#         )

#         if trend == "STRONG UPTREND":

#             st.success(trend)

#         elif trend == "MODERATE UPTREND":

#             st.warning(trend)

#         else:

#             st.error(trend)

#         # ===================================
#         # PATTERN
#         # ===================================

#         st.subheader(
#             "🕯 Candlestick Pattern"
#         )

#         pattern = (
#             score_result[
#                 "pattern"
#             ]
#         )

#         if pattern == "No Pattern":

#             st.info(
#                 "No Major Pattern Detected"
#             )

#         else:

#             st.success(
#                 pattern
#             )

#         # ===================================
#         # RECOMMENDATION
#         # ===================================

#         st.subheader(
#             "🤖 Recommendation"
#         )

#         recommendation = (
#             score_result[
#                 "recommendation"
#             ]
#         )

#         if recommendation == "STRONG BUY":

#             st.success(
#                 recommendation
#             )

#         elif recommendation == "BUY":

#             st.success(
#                 recommendation
#             )

#         elif recommendation == "HOLD":

#             st.warning(
#                 recommendation
#             )

#         else:

#             st.error(
#                 recommendation
#             )

#         # ===================================
#         # SCORE BREAKDOWN
#         # ===================================

#         st.subheader(
#             "📊 Score Breakdown"
#         )

#         st.json({

#             "Trend Score":
#             score_result[
#                 "trend_score"
#             ],

#             "Momentum Score":
#             score_result[
#                 "momentum_score"
#             ],

#             "Volume Score":
#             score_result[
#                 "volume_score"
#             ],

#             "Volatility Score":
#             score_result[
#                 "volatility_score"
#             ],

#             "Strength Score":
#             score_result[
#                 "strength_score"
#             ],

#             "Market Score":
#             score_result[
#                 "market_score"
#             ],

#             "Pattern Score":
#             score_result[
#                 "pattern_score"
#             ],

#             "Multi Timeframe Score":
#             score_result[
#                 "multi_timeframe_score"
#             ],

#             "Total Score":
#             score_result[
#                 "total_score"
#             ]
#         })

#         # ===================================
#         # TRADE PLAN
#         # ===================================

#         st.subheader(
#             "🎯 Trade Plan"
#         )

#         c1, c2, c3 = (
#             st.columns(3)
#         )

#         c1.metric(
#             "Entry",
#             f"₹{trade_plan['entry']}"
#         )

#         c2.metric(
#             "Stop Loss",
#             f"₹{trade_plan['stop_loss']}"
#         )

#         c3.metric(
#             "Target",
#             f"₹{trade_plan['target']}"
#         )

#         c1, c2, c3 = (
#             st.columns(3)
#         )

#         c1.metric(
#             "Risk",
#             f"₹{trade_plan['risk']}"
#         )

#         c2.metric(
#             "Reward",
#             f"₹{trade_plan['reward']}"
#         )

#         c3.metric(
#             "Risk Reward",
#             trade_plan[
#                 "risk_reward"
#             ]
#         )

#         rr = (
#             trade_plan[
#                 "risk_reward"
#             ]
#         )

#         if rr >= 2:

#             st.success(
#                 "Excellent Risk Reward Setup ✅"
#             )

#         elif rr >= 1.5:

#             st.warning(
#                 "Average Risk Reward Setup ⚠️"
#             )

#         else:

#             st.error(
#                 "Poor Risk Reward Setup ❌"
#             )

#         # ===================================
#         # AI EXPLANATION
#         # ===================================

#         st.subheader(
#             "🧠 AI Explanation"
#         )

#         st.success(
#             f"Signal : "
#             f"{ai_result['signal']}"
#         )

#         st.info(
#             f"Confidence : "
#             f"{ai_result['confidence']}%"
#         )

#         for reason in (
#             ai_result["reasons"]
#         ):

#             st.write(
#                 "✅",
#                 reason
#             )

#         # ===================================
#         # INDICATORS
#         # ===================================

#         st.subheader(
#             "📈 Technical Indicators"
#         )

#         ic1, ic2, ic3, ic4 = (
#             st.columns(4)
#         )

#         ic1.metric(
#             "EMA20",
#             round(
#                 latest["EMA20"],
#                 2
#             )
#         )

#         ic2.metric(
#             "EMA50",
#             round(
#                 latest["EMA50"],
#                 2
#             )
#         )

#         ic3.metric(
#             "MACD",
#             round(
#                 latest["MACD"],
#                 2
#             )
#         )

#         ic4.metric(
#             "ATR",
#             round(
#                 latest["ATR"],
#                 2
#             )
#         )

#         # ===================================
#         # CHART
#         # ===================================

#         st.subheader(
#             "📉 Price Chart"
#         )

#         st.line_chart(
#             df["Close"]
#         )

#         # ===================================
#         # DATA
#         # ===================================

#         st.subheader(
#             "📋 Recent Data"
#         )

#         st.dataframe(
#             df.tail(20),
#             use_container_width=True
#         )