import ta


def calculate_indicators(df):

    # EMA
    df["EMA20"] = ta.trend.ema_indicator(
        df["Close"],
        window=20
    )

    df["EMA50"] = ta.trend.ema_indicator(
        df["Close"],
        window=50
    )

    # RSI
    df["RSI"] = ta.momentum.rsi(
        df["Close"],
        window=14
    )

    # MACD
    macd = ta.trend.MACD(df["Close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(
        df["Close"],
        window=20,
        window_dev=2
    )

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    # ATR
    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    # ADX
    adx = ta.trend.ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ADX"] = adx.adx()

    # OBV
    df["OBV"] = ta.volume.on_balance_volume(
        close=df["Close"],
        volume=df["Volume"]
    )

    return df