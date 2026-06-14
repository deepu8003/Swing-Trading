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
        previous = df.iloc[-2]

        trend_score = 0
        momentum_score = 0
        volume_score = 0
        volatility_score = 0
        strength_score = 0
        market_score = 0
        pattern_score = 0
        timeframe_score = 0

        # TREND

        if latest["EMA20"] > latest["EMA50"]:
            trend_score += 20

        if latest["Close"] > latest["EMA20"]:
            trend_score += 10

        # MOMENTUM

        if 55 <= latest["RSI"] <= 70:
            momentum_score += 15

        if latest["MACD"] > latest["MACD_SIGNAL"]:
            momentum_score += 15

        # VOLUME

        avg_volume = (
            df["Volume"]
            .tail(20)
            .mean()
        )

        if latest["Volume"] > avg_volume * 1.5:
            volume_score += 20

        # STRENGTH

        if latest["ADX"] > 25:
            strength_score += 15

        # VOLATILITY

        atr_percent = (
            latest["ATR"]
            /
            latest["Close"]
        ) * 100

        if atr_percent < 5:
            volatility_score += 10

        if latest["Close"] > latest["BB_MIDDLE"]:
            volatility_score += 10

        # MARKET FILTER

        market_result = (
            MarketFilter()
            .get_market_status()
        )

        market_score = (
            market_result["score"]
        )

        # CANDLESTICK

        pattern_result = (
            CandlestickPattern()
            .detect(df)
        )

        pattern_score = (
            pattern_result["score"]
        )

        # MULTI TIMEFRAME

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

        # TOTAL SCORE

        total_score = (

            trend_score

            + momentum_score

            + volume_score

            + volatility_score

            + strength_score

            + market_score

            + pattern_score

            + timeframe_score
        )

        # RECOMMENDATION

        if total_score >= 100:

            recommendation = (
                "STRONG BUY"
            )

        elif total_score >= 75:

            recommendation = (
                "BUY"
            )

        elif total_score >= 50:

            recommendation = (
                "HOLD"
            )

        else:

            recommendation = (
                "SELL"
            )

        return {

            "trend_score":
            trend_score,

            "momentum_score":
            momentum_score,

            "volume_score":
            volume_score,

            "volatility_score":
            volatility_score,

            "strength_score":
            strength_score,

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