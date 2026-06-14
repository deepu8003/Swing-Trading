import pandas as pd

from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer
from strategy.recommendation import RecommendationEngine


class OpportunityScanner:

    def scan(self):

        symbols = [

            "RELIANCE.NS",
            "TCS.NS",
            "INFY.NS",
            "HDFCBANK.NS",
            "ICICIBANK.NS",
            "SBIN.NS",
            "LT.NS",
            "ITC.NS",
            "AXISBANK.NS",
            "KOTAKBANK.NS",
            "BHARTIARTL.NS",
            "HCLTECH.NS",
            "ASIANPAINT.NS",
            "MARUTI.NS",
            "SUNPHARMA.NS"

        ]

        scorer = StockScorer()

        recommender = (
            RecommendationEngine()
        )

        results = []

        for symbol in symbols:

            try:

                print(
                    f"Scanning {symbol}"
                )

                df = download_stock_data(
                    symbol
                )

                if df.empty:
                    continue

                df = calculate_indicators(
                    df
                )

                score = (
                    scorer
                    .calculate_score(
                        df,
                        symbol
                    )
                )

                trade = (
                    recommender
                    .generate_trade_plan(
                        df
                    )
                )

                results.append({

                    "Symbol":
                    symbol,

                    "Score":
                    score[
                        "total_score"
                    ],

                    "Recommendation":
                    score[
                        "recommendation"
                    ],

                    "Pattern":
                    score[
                        "pattern"
                    ],

                    "RiskReward":
                    trade[
                        "risk_reward"
                    ],

                    "Entry":
                    trade[
                        "entry"
                    ],

                    "Target":
                    trade[
                        "target"
                    ]
                })

            except Exception as e:

                print(
                    symbol,
                    str(e)
                )

        result_df = (
            pd.DataFrame(results)
        )

        if result_df.empty:
            return result_df

        result_df = (
            result_df
            .sort_values(
                by=[
                    "Score",
                    "RiskReward"
                ],
                ascending=False
            )
        )

        return result_df