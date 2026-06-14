class SupportResistance:

    def calculate(self, df):

        support = round(
            df["Low"].tail(20).min(),
            2
        )

        resistance = round(
            df["High"].tail(20).max(),
            2
        )

        current_price = round(
            df["Close"].iloc[-1],
            2
        )

        return {
            "current_price": current_price,
            "support": support,
            "resistance": resistance
        }