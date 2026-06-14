from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer

symbol = "TCS.NS"

df = download_stock_data(symbol)

df = calculate_indicators(df)

scorer = StockScorer()

result = scorer.calculate_score(df)

print("\n===== STOCK SCORE =====\n")

for key, value in result.items():
    print(f"{key}: {value}")