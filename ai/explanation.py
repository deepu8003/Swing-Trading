class AIExplanation:

    def generate(self, df):

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        reasons = []
        confidence = 0

        if latest["EMA20"] > latest["EMA50"]:
            reasons.append(
                "EMA20 is above EMA50 (Bullish Trend)"
            )
            confidence += 20

        if latest["Close"] > latest["EMA20"]:
            reasons.append(
                "Price is above EMA20"
            )
            confidence += 15

        if 55 <= latest["RSI"] <= 70:
            reasons.append(
                f"RSI is healthy ({latest['RSI']:.2f})"
            )
            confidence += 15

        if latest["MACD"] > latest["MACD_SIGNAL"]:
            reasons.append(
                "MACD Bullish Crossover"
            )
            confidence += 20

        if latest["OBV"] > previous["OBV"]:
            reasons.append(
                "OBV Increasing"
            )
            confidence += 15

        atr_percent = (
            latest["ATR"] / latest["Close"]
        ) * 100

        if atr_percent < 5:
            reasons.append(
                "Volatility Under Control"
            )
            confidence += 15

        if confidence > 100:
            confidence = 100

        if confidence >= 80:
            signal = "STRONG BUY"
        elif confidence >= 65:
            signal = "BUY"
        elif confidence >= 50:
            signal = "HOLD"
        else:
            signal = "SELL"

        return {
            "signal": signal,
            "confidence": confidence,
            "reasons": reasons
        }