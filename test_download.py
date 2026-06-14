from data.downloader import download_stock_data

df = download_stock_data("TCS.NS")

print(df.tail())