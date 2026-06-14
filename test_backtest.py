from data.downloader import download_stock_data
from backtest.engine import BacktestEngine

symbol = "TCS.NS"

df = download_stock_data(
    symbol,
    period="2y"
)

engine = BacktestEngine()

result = engine.run_backtest(df)

print("\n===== BACKTEST REPORT =====\n")

for key, value in result.items():
    print(f"{key}: {value}")