from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from strategy.recommendation import RecommendationEngine

symbol = "TCS.NS"

df = download_stock_data(symbol)

df = calculate_indicators(df)

engine = RecommendationEngine()

result = engine.generate_trade_plan(df)

print("\n===== TRADE PLAN =====\n")

for k, v in result.items():
    print(f"{k}: {v}")