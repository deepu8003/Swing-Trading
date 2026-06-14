from data.downloader import download_stock_data
from indicators.technical import calculate_indicators
from ai.explanation import AIExplanation

symbol = "TCS.NS"

df = download_stock_data(symbol)

df = calculate_indicators(df)

engine = AIExplanation()

result = engine.generate(df)

print("\n===== AI EXPLANATION =====\n")

print("Signal:", result["signal"])

print("Confidence:", result["confidence"])

print("\nReasons:")

for reason in result["reasons"]:
    print("-", reason)