from data.downloader import download_stock_data
from indicators.technical import calculate_indicators


class MarketFilter:

    def get_market_status(self):

        try:

            df = download_stock_data(
                "^NSEI",
                period="1y"
            )

            if df.empty:
                return {
                    "status": "UNKNOWN",
                    "score": 0
                }

            df = calculate_indicators(df)

            latest = df.iloc[-1]

            if (
                latest["EMA20"] >
                latest["EMA50"]
                and
                latest["RSI"] > 50
            ):

                return {
                    "status": "BULLISH",
                    "score": 20
                }

            elif latest["RSI"] > 45:

                return {
                    "status": "SIDEWAYS",
                    "score": 10
                }

            else:

                return {
                    "status": "BEARISH",
                    "score": 0
                }

        except Exception:

            return {
                "status": "UNKNOWN",
                "score": 0
            }