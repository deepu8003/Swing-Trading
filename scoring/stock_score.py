from market.market_filter import MarketFilter
from strategy.candlestick import CandlestickPattern
from strategy.multi_timeframe import MultiTimeframeAnalysis


class StockScorer:

    def calculate_score(
        self,
        df,
        symbol=None
    ):

        latest = df.iloc[-1]

        trend_score = 0
        structure_score = 0
        momentum_score = 0
        volume_score = 0
        breakout_score = 0
        pullback_score = 0
        volatility_score = 0
        market_score = 0
        pattern_score = 0
        timeframe_score = 0

        # =====================================
        # TREND
        # =====================================

        if latest["Close"] > latest["EMA50"]:
            trend_score += 10

        if latest["EMA50"] > latest["SMA200"]:
            trend_score += 15

        if latest["ADX"] > 25:
            trend_score += 10

        # Maximum = 35

        # =====================================
        # STRUCTURE
        # =====================================

        if (
            latest["HIGHER_HIGH"]
            and
            latest["HIGHER_LOW"]
        ):
            structure_score += 15

        # =====================================
        # MOMENTUM
        # =====================================

        # RSI

        if 50 < latest["RSI"] < 70:
            momentum_score += 10

        elif (
            40 <= latest["RSI"] <= 50
            and
            latest["UPTREND"]
        ):
            momentum_score += 15

        # MACD

        if (
            latest["MACD"] > latest["MACD_SIGNAL"]
            and
            latest["MACD"] > 0
            and
            latest["MACD_SIGNAL"] > 0
        ):
            momentum_score += 15

        # =====================================
        # VOLUME
        # =====================================

        if latest["VOL_RATIO"] > 1.75:
            volume_score += 20

        # =====================================
        # BREAKOUT
        # =====================================

        if latest["BREAKOUT"]:
            breakout_score += 20

        # =====================================
        # PULLBACK
        # =====================================

        if latest["PULLBACK"]:
            pullback_score += 15

        # =====================================
        # VOLATILITY
        # =====================================

        atr_percent = (
            latest["ATR"]
            /
            latest["Close"]
        ) * 100

        if atr_percent < 6:
            volatility_score += 10

        # =====================================
        # MARKET FILTER
        # =====================================

        market_result = (
            MarketFilter()
            .get_market_status()
        )

        market_score = (
            market_result["score"]
        )

        # =====================================
        # CANDLESTICK PATTERN
        # =====================================

        pattern_result = (
            CandlestickPattern()
            .detect(df)
        )

        pattern_score = (
            pattern_result["score"]
        )

        # =====================================
        # MULTI-TIMEFRAME
        # =====================================

        timeframe_result = {
            "trend": "UNKNOWN",
            "score": 0
        }

        if symbol:

            timeframe_result = (
                MultiTimeframeAnalysis()
                .analyze(symbol)
            )

            timeframe_score = (
                timeframe_result["score"]
            )

        # =====================================
        # TOTAL SCORE
        # =====================================

        total_score = (

            trend_score

            + structure_score

            + momentum_score

            + volume_score

            + breakout_score

            + pullback_score

            + volatility_score

            + market_score

            + pattern_score

            + timeframe_score
        )

        # =====================================
        # RECOMMENDATION
        # =====================================

        if total_score >= 120:

            recommendation = (
                "STRONG BUY"
            )

        elif total_score >= 90:

            recommendation = (
                "BUY"
            )

        elif total_score >= 70:

            recommendation = (
                "WATCHLIST"
            )

        else:

            recommendation = (
                "AVOID"
            )

        return {

            "trend_score":
            trend_score,

            "structure_score":
            structure_score,

            "momentum_score":
            momentum_score,

            "volume_score":
            volume_score,

            "breakout_score":
            breakout_score,

            "pullback_score":
            pullback_score,

            "volatility_score":
            volatility_score,

            "market_score":
            market_score,

            "market_status":
            market_result["status"],

            "pattern":
            pattern_result["pattern"],

            "pattern_score":
            pattern_score,

            "multi_timeframe":
            timeframe_result["trend"],

            "multi_timeframe_score":
            timeframe_score,

            "total_score":
            total_score,

            "recommendation":
            recommendation
        }


# from market.market_filter import MarketFilter
# from strategy.candlestick import CandlestickPattern
# from strategy.multi_timeframe import MultiTimeframeAnalysis


# # ======================================================
# # WEIGHT TABLE  (must sum to 1.0)
# # ======================================================

# WEIGHTS = {
#     "trend":     0.35,
#     "momentum":  0.25,
#     "volume":    0.20,
#     "breakout":  0.10,
#     "risk":      0.10,
# }


# class StockScorer:
#     """
#     Composite scorer that returns a 0-100 final score
#     built from five independently normalised sub-scores.

#     All sub-scores are also on a 0-100 scale so they are
#     easy to explain to beginner investors.
#     """

#     def calculate_score(self, df, symbol=None):

#         latest   = df.iloc[-1]
#         previous = df.iloc[-2]

#         # --------------------------------------------------
#         # 1. TREND SCORE  (0-100)
#         # --------------------------------------------------

#         trend_score, trend_label, trend_details = (
#             self._score_trend(df, latest)
#         )

#         # --------------------------------------------------
#         # 2. MOMENTUM SCORE  (0-100)
#         # --------------------------------------------------

#         momentum_score, momentum_label, momentum_details = (
#             self._score_momentum(latest, previous)
#         )

#         # --------------------------------------------------
#         # 3. VOLUME SCORE  (0-100)
#         # --------------------------------------------------

#         volume_score, volume_label, volume_details = (
#             self._score_volume(df, latest)
#         )

#         # --------------------------------------------------
#         # 4. BREAKOUT STRENGTH SCORE  (0-100)
#         # --------------------------------------------------

#         breakout_score, breakout_label, breakout_details = (
#             self._score_breakout(df, latest)
#         )

#         # --------------------------------------------------
#         # 5. RISK SCORE  (0-100, higher = lower risk)
#         # --------------------------------------------------

#         risk_score, risk_label, risk_details = (
#             self._score_risk(latest)
#         )

#         # --------------------------------------------------
#         # MARKET FILTER  (applied as a multiplier, not addend)
#         # --------------------------------------------------

#         market_result = (
#             MarketFilter()
#             .get_market_status()
#         )
#         market_status = market_result["status"]

#         # Bearish market dampens the final score by 15 %
#         market_multiplier = {
#             "BULLISH":  1.00,
#             "SIDEWAYS": 0.92,
#             "BEARISH":  0.85,
#             "UNKNOWN":  0.95,
#         }.get(market_status, 0.95)

#         # --------------------------------------------------
#         # CANDLESTICK PATTERN  (bonus, max +5 pts)
#         # --------------------------------------------------

#         pattern_result = (
#             CandlestickPattern()
#             .detect(df)
#         )
#         pattern_bonus = min(pattern_result["score"], 5)

#         # --------------------------------------------------
#         # MULTI-TIMEFRAME  (bonus, max +5 pts)
#         # --------------------------------------------------

#         timeframe_result = {
#             "trend": "UNKNOWN",
#             "score": 0
#         }
#         if symbol:
#             timeframe_result = (
#                 MultiTimeframeAnalysis()
#                 .analyze(symbol)
#             )

#         # Map multi-timeframe score (0-20 in original) → 0-5
#         tf_bonus = min(timeframe_result["score"] / 4, 5)

#         # --------------------------------------------------
#         # COMPOSITE SCORE
#         # --------------------------------------------------

#         raw_score = (
#             trend_score    * WEIGHTS["trend"]
#             + momentum_score * WEIGHTS["momentum"]
#             + volume_score   * WEIGHTS["volume"]
#             + breakout_score * WEIGHTS["breakout"]
#             + risk_score     * WEIGHTS["risk"]
#         )

#         # Apply market multiplier, then add bonuses
#         composite = raw_score * market_multiplier
#         composite += pattern_bonus + tf_bonus

#         # Clamp to [0, 100]
#         final_score = min(max(round(composite, 1), 0), 100)

#         # --------------------------------------------------
#         # CLASSIFICATION
#         # --------------------------------------------------

#         classification = self._classify(final_score)
#         recommendation = self._recommend(final_score)

#         # Success probability: smoothed logistic curve
#         # anchored so that 70 → ~65 %, 90 → ~85 %
#         success_probability = round(
#             100 / (1 + 2.718 ** (-(final_score - 50) / 15)),
#             1
#         )

#         # --------------------------------------------------
#         # TRADE SETUP  (Entry / SL / Target)
#         # --------------------------------------------------

#         trade_setup = self._build_trade_setup(
#             df, latest
#         )

#         return {
#             # Sub-scores (each 0-100)
#             "trend_score":    trend_score,
#             "momentum_score": momentum_score,
#             "volume_score":   volume_score,
#             "breakout_score": breakout_score,
#             "risk_score":     risk_score,

#             # Sub-labels
#             "trend_label":    trend_label,
#             "momentum_label": momentum_label,
#             "volume_label":   volume_label,
#             "risk_label":     risk_label,
#             "breakout_label": breakout_label,

#             # Detail dicts (each key → bool or float)
#             "trend_details":    trend_details,
#             "momentum_details": momentum_details,
#             "volume_details":   volume_details,
#             "risk_details":     risk_details,
#             "breakout_details": breakout_details,

#             # Bonuses
#             "pattern":       pattern_result["pattern"],
#             "pattern_score": pattern_result["score"],
#             "multi_timeframe":       timeframe_result["trend"],
#             "multi_timeframe_score": timeframe_result["score"],

#             # Market context
#             "market_status": market_status,
#             "market_score":  market_result["score"],

#             # Final output
#             "total_score":         final_score,
#             "classification":      classification,
#             "recommendation":      recommendation,
#             "success_probability": success_probability,

#             # Trade setup
#             "trade_setup": trade_setup,
#         }

#     # ==================================================
#     # SUB-SCORERS
#     # ==================================================

#     def _score_trend(self, df, latest):
#         """
#         Evaluate the direction and strength of the trend
#         using EMAs, SMAs, and cross signals.

#         Returns (score 0-100, label str, details dict).
#         """

#         points = 0
#         details = {}

#         # EMA alignment  (35 pts)
#         ema_bull = (
#             latest["EMA20"] > latest["EMA50"]
#         )
#         details["ema20_above_ema50"] = ema_bull
#         if ema_bull:
#             points += 20

#         close_above_ema20 = (
#             latest["Close"] > latest["EMA20"]
#         )
#         details["close_above_ema20"] = close_above_ema20
#         if close_above_ema20:
#             points += 15

#         # SMA200 long-term trend  (20 pts)
#         above_sma200 = bool(latest.get("ABOVE_SMA200", False))
#         details["above_sma200"] = above_sma200
#         if above_sma200:
#             points += 20

#         # SMA20 > SMA50  (15 pts)
#         sma_bull = (
#             latest.get("SMA20", 0) > latest.get("SMA50", 0)
#         )
#         details["sma20_above_sma50"] = sma_bull
#         if sma_bull:
#             points += 15

#         # Close above SMA50  (10 pts)
#         close_above_sma50 = (
#             latest["Close"] > latest.get("SMA50", latest["Close"])
#         )
#         details["close_above_sma50"] = close_above_sma50
#         if close_above_sma50:
#             points += 10

#         # Recent Golden Cross in last 10 bars  (+10 bonus)
#         recent = df.tail(10)
#         if "GOLDEN_CROSS" in df.columns:
#             if recent["GOLDEN_CROSS"].any():
#                 details["golden_cross"] = True
#                 points += 10
#             elif "DEATH_CROSS" in df.columns and recent["DEATH_CROSS"].any():
#                 details["death_cross"] = True
#                 points -= 10
#             else:
#                 details["golden_cross"] = False
#                 details["death_cross"]  = False

#         score = min(max(points, 0), 100)

#         if score >= 80:
#             label = "Strong Bullish"
#         elif score >= 60:
#             label = "Bullish"
#         elif score >= 40:
#             label = "Neutral"
#         elif score >= 20:
#             label = "Bearish"
#         else:
#             label = "Strong Bearish"

#         return score, label, details

#     def _score_momentum(self, latest, previous):
#         """
#         Score RSI, MACD line, MACD histogram, and ADX.

#         Returns (score 0-100, label str, details dict).
#         """

#         points = 0
#         details = {}

#         rsi = latest["RSI"]

#         # RSI  (30 pts, graduated)
#         details["rsi"] = round(float(rsi), 2)

#         if 55 <= rsi <= 70:
#             # Sweet spot: trending up, not overbought
#             points += 30
#             details["rsi_zone"] = "Bullish"
#         elif 50 <= rsi < 55:
#             # Just crossed bullish threshold
#             points += 20
#             details["rsi_zone"] = "Mildly Bullish"
#         elif 45 <= rsi < 50:
#             # Neutral territory
#             points += 10
#             details["rsi_zone"] = "Neutral"
#         elif rsi > 70:
#             # Overbought — some risk of reversal
#             points += 15
#             details["rsi_zone"] = "Overbought"
#         elif rsi < 30:
#             # Oversold bounce potential
#             points += 10
#             details["rsi_zone"] = "Oversold"
#         else:
#             details["rsi_zone"] = "Weak"

#         # MACD line above signal  (25 pts)
#         macd_bull = (
#             latest["MACD"] > latest["MACD_SIGNAL"]
#         )
#         details["macd_above_signal"] = macd_bull
#         if macd_bull:
#             points += 25

#         # MACD histogram expanding (momentum accelerating)  (20 pts)
#         hist_curr = latest["MACD_HIST"]
#         hist_prev = previous["MACD_HIST"]
#         hist_expanding = (
#             hist_curr > 0 and hist_curr > hist_prev
#         )
#         details["macd_hist_expanding"] = hist_expanding
#         details["macd_hist"] = round(float(hist_curr), 4)
#         if hist_expanding:
#             points += 20

#         # ADX  (25 pts, graduated)
#         adx = latest["ADX"]
#         details["adx"] = round(float(adx), 2)

#         if adx >= 40:
#             points += 25
#             details["adx_strength"] = "Very Strong Trend"
#         elif adx >= 25:
#             points += 20
#             details["adx_strength"] = "Strong Trend"
#         elif adx >= 20:
#             points += 10
#             details["adx_strength"] = "Developing Trend"
#         else:
#             details["adx_strength"] = "Weak / No Trend"

#         score = min(max(points, 0), 100)

#         if score >= 75:
#             label = "Strong Momentum"
#         elif score >= 50:
#             label = "Positive Momentum"
#         elif score >= 30:
#             label = "Weak Momentum"
#         else:
#             label = "No Momentum"

#         return score, label, details

#     def _score_volume(self, df, latest):
#         """
#         Score using relative volume, spike detection,
#         and OBV trend confirmation.

#         Returns (score 0-100, label str, details dict).
#         """

#         points = 0
#         details = {}

#         rel_vol = float(latest.get("REL_VOL", 1.0))
#         details["relative_volume"] = round(rel_vol, 2)

#         # Relative volume tiers  (40 pts)
#         if rel_vol >= 3.0:
#             points += 40
#             details["volume_tier"] = "Extreme Spike (3x+)"
#         elif rel_vol >= 2.0:
#             points += 30
#             details["volume_tier"] = "Strong Spike (2x+)"
#         elif rel_vol >= 1.5:
#             points += 20
#             details["volume_tier"] = "Above Average (1.5x+)"
#         elif rel_vol >= 1.0:
#             points += 10
#             details["volume_tier"] = "Average"
#         else:
#             details["volume_tier"] = "Below Average"

#         # Volume spike on a green candle = bullish confirmation  (25 pts)
#         green_candle = latest["Close"] > latest.get(
#             "Open", latest["Close"]
#         )
#         volume_spike = rel_vol >= 1.5
#         breakout_vol = green_candle and volume_spike
#         details["breakout_volume_confirmed"] = breakout_vol
#         if breakout_vol:
#             points += 25

#         # OBV rising over last 10 bars  (20 pts)
#         if "OBV" in df.columns and len(df) >= 10:
#             obv_now  = df["OBV"].iloc[-1]
#             obv_prev = df["OBV"].iloc[-10]
#             obv_rising = obv_now > obv_prev
#             details["obv_rising"] = obv_rising
#             if obv_rising:
#                 points += 20

#         # Consistent above-average volume (last 5 bars ≥ 1.2x avg)  (15 pts)
#         if "REL_VOL" in df.columns and len(df) >= 5:
#             above_avg_count = int(
#                 (df["REL_VOL"].tail(5) >= 1.2).sum()
#             )
#             details["above_avg_vol_days"] = above_avg_count
#             if above_avg_count >= 4:
#                 points += 15
#             elif above_avg_count >= 2:
#                 points += 8

#         score = min(max(points, 0), 100)

#         if score >= 75:
#             label = "Very High Volume"
#         elif score >= 50:
#             label = "High Volume"
#         elif score >= 30:
#             label = "Average Volume"
#         else:
#             label = "Low Volume"

#         return score, label, details

#     def _score_risk(self, latest):
#         """
#         Higher score = LOWER risk (safer to trade).

#         Evaluated via ATR%, Bollinger Band position,
#         and +DI vs -DI directional bias.

#         Returns (score 0-100, label str, details dict).
#         """

#         points = 0
#         details = {}

#         # ATR%  (40 pts — lower ATR% = less risk)
#         atr_pct = float(latest.get("ATR_PCT", 5.0))
#         details["atr_pct"] = round(atr_pct, 2)

#         if atr_pct < 1.5:
#             points += 40
#             details["volatility_tier"] = "Low"
#         elif atr_pct < 3.0:
#             points += 25
#             details["volatility_tier"] = "Moderate"
#         elif atr_pct < 5.0:
#             points += 10
#             details["volatility_tier"] = "High"
#         else:
#             details["volatility_tier"] = "Very High"

#         # Price position inside Bollinger Bands  (30 pts)
#         bb_upper  = latest.get("BB_UPPER",  latest["Close"] * 1.1)
#         bb_lower  = latest.get("BB_LOWER",  latest["Close"] * 0.9)
#         bb_middle = latest.get("BB_MIDDLE", latest["Close"])

#         above_mid = latest["Close"] > bb_middle
#         not_extended = latest["Close"] < bb_upper * 0.98

#         details["above_bb_middle"]  = bool(above_mid)
#         details["not_bb_extended"]  = bool(not_extended)

#         if above_mid and not_extended:
#             points += 30  # Ideal: above mid, not at top
#         elif above_mid:
#             points += 15  # Above mid but near upper → risky
#         elif not_extended:
#             points += 10  # Below mid but room to fall

#         # Directional bias: +DI > -DI  (30 pts)
#         di_pos = float(latest.get("DI_POS", 0))
#         di_neg = float(latest.get("DI_NEG", 0))
#         bullish_di = di_pos > di_neg
#         details["di_pos"] = round(di_pos, 2)
#         details["di_neg"] = round(di_neg, 2)
#         details["bullish_di"] = bullish_di
#         if bullish_di:
#             points += 30

#         score = min(max(points, 0), 100)

#         if score >= 70:
#             risk_label = "Low Risk"
#         elif score >= 40:
#             risk_label = "Medium Risk"
#         else:
#             risk_label = "High Risk"

#         return score, risk_label, details

#     def _score_breakout(self, df, latest):
#         """
#         Detect price breakout above resistance or
#         Bollinger Band squeeze expansion.

#         Returns (score 0-100, label str, details dict).
#         """

#         points = 0
#         details = {}

#         close       = float(latest["Close"])
#         resistance  = df.attrs.get("RESISTANCE", close * 1.05)
#         support     = df.attrs.get("SUPPORT",    close * 0.95)

#         details["resistance"] = round(resistance, 2)
#         details["support"]    = round(support, 2)

#         # Price breaking above resistance  (50 pts)
#         breakout_margin = resistance * 0.005  # 0.5 % tolerance
#         above_resistance = close > (resistance - breakout_margin)
#         details["price_above_resistance"] = above_resistance
#         if above_resistance:
#             points += 50

#         # Above support (not near breakdown)  (20 pts)
#         near_support = close < support * 1.03
#         details["near_support"] = near_support
#         if not near_support:
#             points += 20

#         # Bollinger Band squeeze breakout  (30 pts)
#         # Squeeze: BB width contracted, then price moves above upper
#         if "BB_WIDTH" in df.columns and len(df) >= 20:
#             avg_bb_width = float(
#                 df["BB_WIDTH"].tail(20).mean()
#             )
#             curr_bb_width = float(
#                 latest.get("BB_WIDTH", avg_bb_width)
#             )
#             bb_expanding = curr_bb_width > avg_bb_width * 1.1

#             bb_upper = float(
#                 latest.get("BB_UPPER", close)
#             )
#             bb_breakout = close > bb_upper * 0.99

#             details["bb_squeeze_breakout"] = (
#                 bb_expanding and bb_breakout
#             )
#             if bb_expanding and bb_breakout:
#                 points += 30

#         score = min(max(points, 0), 100)

#         if score >= 70:
#             label = "Strong Breakout"
#         elif score >= 40:
#             label = "Potential Breakout"
#         elif score >= 20:
#             label = "No Breakout"
#         else:
#             label = "Near Support"

#         return score, label, details

#     def _build_trade_setup(self, df, latest):
#         """
#         Generate Entry / Stop Loss / Target based on
#         ATR and Support/Resistance levels.
#         """

#         close      = float(latest["Close"])
#         atr        = float(latest.get("ATR", close * 0.02))
#         support    = df.attrs.get("SUPPORT",    close - atr * 2)
#         resistance = df.attrs.get("RESISTANCE", close + atr * 3)

#         entry      = round(close, 2)
#         stop_loss  = round(max(close - atr * 1.5, support * 0.99), 2)
#         target     = round(
#             min(close + atr * 3, resistance * 1.005), 2
#         )

#         risk       = round(entry - stop_loss, 2)
#         reward     = round(target - entry, 2)
#         risk_reward = round(reward / risk, 2) if risk > 0 else 0
#         expected_return = round((reward / entry) * 100, 2)

#         return {
#             "entry":           entry,
#             "stop_loss":       stop_loss,
#             "target":          target,
#             "risk":            risk,
#             "reward":          reward,
#             "risk_reward":     risk_reward,
#             "expected_return": expected_return,
#         }

#     # ==================================================
#     # CLASSIFICATION HELPERS
#     # ==================================================

#     @staticmethod
#     def _classify(score):
#         if score >= 90:
#             return "Exceptional"
#         elif score >= 80:
#             return "Strong Buy"
#         elif score >= 70:
#             return "Buy"
#         elif score >= 60:
#             return "Watchlist"
#         else:
#             return "Avoid"

#     @staticmethod
#     def _recommend(score):
#         """
#         Backward-compatible recommendation string
#         used by the existing Streamlit page.
#         """
#         if score >= 80:
#             return "STRONG BUY"
#         elif score >= 70:
#             return "BUY"
#         elif score >= 60:
#             return "HOLD"
#         else:
#             return "SELL"


# # from market.market_filter import MarketFilter
# # from strategy.candlestick import CandlestickPattern
# # from strategy.multi_timeframe import MultiTimeframeAnalysis


# # class StockScorer:

# #     def calculate_score(
# #         self,
# #         df,
# #         symbol=None
# #     ):

# #         latest = df.iloc[-1]
# #         previous = df.iloc[-2]

# #         trend_score = 0
# #         momentum_score = 0
# #         volume_score = 0
# #         volatility_score = 0
# #         strength_score = 0
# #         market_score = 0
# #         pattern_score = 0
# #         timeframe_score = 0

# #         # TREND

# #         if latest["EMA20"] > latest["EMA50"]:
# #             trend_score += 20

# #         if latest["Close"] > latest["EMA20"]:
# #             trend_score += 10

# #         # MOMENTUM

# #         if 55 <= latest["RSI"] <= 70:
# #             momentum_score += 15

# #         if latest["MACD"] > latest["MACD_SIGNAL"]:
# #             momentum_score += 15

# #         # VOLUME

# #         avg_volume = (
# #             df["Volume"]
# #             .tail(20)
# #             .mean()
# #         )

# #         if latest["Volume"] > avg_volume * 1.5:
# #             volume_score += 20

# #         # STRENGTH

# #         if latest["ADX"] > 25:
# #             strength_score += 15

# #         # VOLATILITY

# #         atr_percent = (
# #             latest["ATR"]
# #             /
# #             latest["Close"]
# #         ) * 100

# #         if atr_percent < 5:
# #             volatility_score += 10

# #         if latest["Close"] > latest["BB_MIDDLE"]:
# #             volatility_score += 10

# #         # MARKET FILTER

# #         market_result = (
# #             MarketFilter()
# #             .get_market_status()
# #         )

# #         market_score = (
# #             market_result["score"]
# #         )

# #         # CANDLESTICK

# #         pattern_result = (
# #             CandlestickPattern()
# #             .detect(df)
# #         )

# #         pattern_score = (
# #             pattern_result["score"]
# #         )

# #         # MULTI TIMEFRAME

# #         timeframe_result = {
# #             "trend": "UNKNOWN",
# #             "score": 0
# #         }

# #         if symbol:

# #             timeframe_result = (
# #                 MultiTimeframeAnalysis()
# #                 .analyze(symbol)
# #             )

# #             timeframe_score = (
# #                 timeframe_result["score"]
# #             )

# #         # TOTAL SCORE

# #         total_score = (

# #             trend_score

# #             + momentum_score

# #             + volume_score

# #             + volatility_score

# #             + strength_score

# #             + market_score

# #             + pattern_score

# #             + timeframe_score
# #         )

# #         # RECOMMENDATION

# #         if total_score >= 100:

# #             recommendation = (
# #                 "STRONG BUY"
# #             )

# #         elif total_score >= 75:

# #             recommendation = (
# #                 "BUY"
# #             )

# #         elif total_score >= 50:

# #             recommendation = (
# #                 "HOLD"
# #             )

# #         else:

# #             recommendation = (
# #                 "SELL"
# #             )

# #         return {

# #             "trend_score":
# #             trend_score,

# #             "momentum_score":
# #             momentum_score,

# #             "volume_score":
# #             volume_score,

# #             "volatility_score":
# #             volatility_score,

# #             "strength_score":
# #             strength_score,

# #             "market_score":
# #             market_score,

# #             "market_status":
# #             market_result["status"],

# #             "pattern":
# #             pattern_result["pattern"],

# #             "pattern_score":
# #             pattern_score,

# #             "multi_timeframe":
# #             timeframe_result["trend"],

# #             "multi_timeframe_score":
# #             timeframe_score,

# #             "total_score":
# #             total_score,

# #             "recommendation":
# #             recommendation
# #         }
