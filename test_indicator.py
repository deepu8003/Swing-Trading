from data.downloader import download_stock_data

from indicators.technical import add_indicators


df = download_stock_data("TCS.NS")

df = add_indicators(df)

print(df.tail())