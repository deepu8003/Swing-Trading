class CandlestickPattern:

    def detect(self, df):

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        # Bullish Engulfing

        if (
            previous["Close"] < previous["Open"]
            and
            latest["Close"] > latest["Open"]
            and
            latest["Close"] > previous["Open"]
            and
            latest["Open"] < previous["Close"]
        ):

            return {
                "pattern": "Bullish Engulfing",
                "score": 15
            }

        # Hammer

        body = abs(
            latest["Close"]
            - latest["Open"]
        )

        lower_shadow = min(
            latest["Close"],
            latest["Open"]
        ) - latest["Low"]

        if lower_shadow > body * 2:

            return {
                "pattern": "Hammer",
                "score": 10
            }

        return {
            "pattern": "No Pattern",
            "score": 0
        }