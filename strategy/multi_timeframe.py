from data.downloader import download_stock_data
from indicators.technical import calculate_indicators


class MultiTimeframeAnalysis:

    def analyze(self, symbol):

        try:

            # =====================================
            # DAILY DATA
            # =====================================

            daily_df = download_stock_data(
                symbol=symbol,
                period="1y",
                interval="1d"
            )

            if daily_df.empty:

                return {
                    "trend": "UNKNOWN",
                    "score": 0
                }

            daily_df = calculate_indicators(
                daily_df
            )

            daily_latest = (
                daily_df.iloc[-1]
            )

            daily_bullish = (

                daily_latest["Close"]
                >
                daily_latest["EMA20"]

                and

                daily_latest["EMA20"]
                >
                daily_latest["EMA50"]

                and

                daily_latest["EMA50"]
                >
                daily_latest["SMA200"]
            )

            # =====================================
            # WEEKLY DATA
            # =====================================

            weekly_df = download_stock_data(
                symbol=symbol,
                period="5y",
                interval="1wk"
            )

            if weekly_df.empty:

                return {
                    "trend": "UNKNOWN",
                    "score": 0
                }

            weekly_df = calculate_indicators(
                weekly_df
            )

            weekly_latest = (
                weekly_df.iloc[-1]
            )

            weekly_bullish = (

                weekly_latest["Close"]
                >
                weekly_latest["EMA20"]

                and

                weekly_latest["EMA20"]
                >
                weekly_latest["EMA50"]

                and

                weekly_latest["EMA50"]
                >
                weekly_latest["SMA200"]
            )

            # =====================================
            # SCORING
            # =====================================

            if (
                weekly_bullish
                and
                daily_bullish
            ):

                return {
                    "trend": "STRONG UPTREND",
                    "score": 20
                }

            elif weekly_bullish:

                return {
                    "trend": "WEEKLY UPTREND",
                    "score": 15
                }

            elif daily_bullish:

                return {
                    "trend": "DAILY UPTREND",
                    "score": 10
                }

            else:

                return {
                    "trend": "DOWNTREND",
                    "score": 0
                }

        except Exception as e:

            print(
                "Multi Timeframe Error:",
                str(e)
            )

            return {
                "trend": "UNKNOWN",
                "score": 0
            }

# from data.downloader import download_stock_data
# from indicators.technical import calculate_indicators


# class MultiTimeframeAnalysis:

#     def analyze(self, symbol):

#         try:

#             # DAILY DATA

#             daily_df = download_stock_data(
#                 symbol=symbol,
#                 period="1y",
#                 interval="1d"
#             )

#             if daily_df.empty:

#                 return {
#                     "trend": "UNKNOWN",
#                     "score": 0
#                 }

#             daily_df = calculate_indicators(
#                 daily_df
#             )

#             daily_latest = (
#                 daily_df.iloc[-1]
#             )

#             daily_bullish = (
#                 daily_latest["EMA20"]
#                 >
#                 daily_latest["EMA50"]
#             )

#             # WEEKLY DATA

#             weekly_df = download_stock_data(
#                 symbol=symbol,
#                 period="2y",
#                 interval="1wk"
#             )

#             if weekly_df.empty:

#                 return {
#                     "trend": "UNKNOWN",
#                     "score": 0
#                 }

#             weekly_df = calculate_indicators(
#                 weekly_df
#             )

#             weekly_latest = (
#                 weekly_df.iloc[-1]
#             )

#             weekly_bullish = (
#                 weekly_latest["EMA20"]
#                 >
#                 weekly_latest["EMA50"]
#             )

#             if (
#                 daily_bullish
#                 and
#                 weekly_bullish
#             ):

#                 return {
#                     "trend": "STRONG UPTREND",
#                     "score": 20
#                 }

#             elif (
#                 daily_bullish
#                 or
#                 weekly_bullish
#             ):

#                 return {
#                     "trend": "MODERATE UPTREND",
#                     "score": 10
#                 }

#             else:

#                 return {
#                     "trend": "DOWNTREND",
#                     "score": 0
#                 }

#         except Exception as e:

#             print(
#                 "Multi Timeframe Error:",
#                 str(e)
#             )

#             return {
#                 "trend": "UNKNOWN",
#                 "score": 0
#             }
