import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer

NIFTY50 = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "LT.NS",
    "SBIN.NS",
    "ITC.NS",
    "BHARTIARTL.NS",
    "HINDUNILVR.NS"
]


def run_scanner():

    scorer = StockScorer()
    results = []

    for symbol in NIFTY50:

        try:

            print(f"Analyzing {symbol}")

            df = download_stock_data(symbol)

            if df.empty:
                continue

            df = calculate_indicators(df)

            result = scorer.calculate_score(df)

            result["symbol"] = symbol

            results.append(result)

        except Exception as e:

            print(f"Error in {symbol}: {e}")

    results.sort(
        key=lambda x: x["total_score"],
        reverse=True
    )

    print("\n===== TOP STOCKS =====\n")

    for stock in results:

        print(
            f"{stock['symbol']} | "
            f"Score: {stock['total_score']} | "
            f"{stock['recommendation']}"
        )


if __name__ == "__main__":
    run_scanner()