import ta
import numpy as np


def calculate_indicators(df):

    # ==========================
    # TREND INDICATORS
    # ==========================

    # EMA
    df["EMA20"] = ta.trend.ema_indicator(
        close=df["Close"],
        window=20
    )

    df["EMA50"] = ta.trend.ema_indicator(
        close=df["Close"],
        window=50
    )

    # Long-term trend
    df["SMA200"] = ta.trend.sma_indicator(
        close=df["Close"],
        window=200
    )

    # ==========================
    # MOMENTUM
    # ==========================

    df["RSI"] = ta.momentum.rsi(
        close=df["Close"],
        window=14
    )

    macd = ta.trend.MACD(
        close=df["Close"]
    )

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    # ==========================
    # VOLATILITY
    # ==========================

    bb = ta.volatility.BollingerBands(
        close=df["Close"],
        window=20,
        window_dev=2
    )

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    # ==========================
    # TREND STRENGTH
    # ==========================

    adx = ta.trend.ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ADX"] = adx.adx()

    # ==========================
    # VOLUME
    # ==========================

    df["OBV"] = ta.volume.on_balance_volume(
        close=df["Close"],
        volume=df["Volume"]
    )

    # 20-day average volume
    df["VOL_AVG20"] = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    # Volume ratio
    df["VOL_RATIO"] = (
        df["Volume"] /
        df["VOL_AVG20"]
    )

    # ==========================
    # SUPPORT / RESISTANCE
    # ==========================

    df["RESISTANCE"] = (
        df["High"]
        .rolling(20)
        .max()
        .shift(1)
    )

    df["SUPPORT"] = (
        df["Low"]
        .rolling(20)
        .min()
        .shift(1)
    )

    # ==========================
    # STRUCTURE
    # ==========================

    df["HIGHER_HIGH"] = (
        df["High"] >
        df["High"].shift(5)
    )

    df["HIGHER_LOW"] = (
        df["Low"] >
        df["Low"].shift(5)
    )

    # ==========================
    # TREND FLAGS
    # ==========================

    df["UPTREND"] = (
        (df["Close"] > df["EMA50"]) &
        (df["EMA50"] > df["SMA200"])
    )

    df["DOWNTREND"] = (
        (df["Close"] < df["EMA50"]) &
        (df["EMA50"] < df["SMA200"])
    )

    # ==========================
    # BREAKOUT
    # ==========================

    df["BREAKOUT"] = (
        (df["Close"] > df["RESISTANCE"]) &
        (df["VOL_RATIO"] > 1.5)
    )

    # ==========================
    # PULLBACK SETUP
    # ==========================

    df["PULLBACK"] = (
        (df["Close"] > df["EMA50"]) &
        (df["Close"] <= df["EMA20"] * 1.02)
    )

    return df

# import numpy as np
# import ta


# def calculate_indicators(df):
#     """
#     Calculate all technical indicators used across the
#     scoring engine, market filter, and analysis page.

#     Adds to the DataFrame (in-place) and returns it.
#     """

#     close = df["Close"]
#     high  = df["High"]
#     low   = df["Low"]
#     vol   = df["Volume"]

#     # --------------------------------------------------
#     # MOVING AVERAGES
#     # --------------------------------------------------

#     # Short-term EMAs (existing — kept for compatibility)
#     df["EMA20"] = ta.trend.ema_indicator(close, window=20)
#     df["EMA50"] = ta.trend.ema_indicator(close, window=50)

#     # Simple Moving Averages (new)
#     df["SMA20"]  = close.rolling(window=20).mean()
#     df["SMA50"]  = close.rolling(window=50).mean()
#     df["SMA200"] = close.rolling(window=200).mean()

#     # --------------------------------------------------
#     # GOLDEN CROSS / DEATH CROSS  (new)
#     # True on the bar where the crossover first occurs.
#     # --------------------------------------------------

#     sma50_prev  = df["SMA50"].shift(1)
#     sma200_prev = df["SMA200"].shift(1)

#     df["GOLDEN_CROSS"] = (
#         (df["SMA50"] > df["SMA200"]) &
#         (sma50_prev <= sma200_prev)
#     )

#     df["DEATH_CROSS"] = (
#         (df["SMA50"] < df["SMA200"]) &
#         (sma50_prev >= sma200_prev)
#     )

#     # Whether SMA50 is currently above SMA200
#     # (used by trend scorer even when no fresh cross)
#     df["ABOVE_SMA200"] = df["SMA50"] > df["SMA200"]

#     # --------------------------------------------------
#     # MOMENTUM
#     # --------------------------------------------------

#     df["RSI"] = ta.momentum.rsi(close, window=14)

#     macd = ta.trend.MACD(close)
#     df["MACD"]        = macd.macd()
#     df["MACD_SIGNAL"] = macd.macd_signal()
#     df["MACD_HIST"]   = macd.macd_diff()

#     # --------------------------------------------------
#     # BOLLINGER BANDS
#     # --------------------------------------------------

#     bb = ta.volatility.BollingerBands(
#         close, window=20, window_dev=2
#     )
#     df["BB_UPPER"]  = bb.bollinger_hband()
#     df["BB_MIDDLE"] = bb.bollinger_mavg()
#     df["BB_LOWER"]  = bb.bollinger_lband()
#     df["BB_WIDTH"]  = (
#         (df["BB_UPPER"] - df["BB_LOWER"])
#         / df["BB_MIDDLE"]
#     ) * 100                              # % of mid-band

#     # --------------------------------------------------
#     # VOLATILITY
#     # --------------------------------------------------

#     atr = ta.volatility.AverageTrueRange(
#         high=high, low=low, close=close, window=14
#     )
#     df["ATR"] = atr.average_true_range()

#     # ATR as a % of price  →  volatility normalised
#     df["ATR_PCT"] = (df["ATR"] / close) * 100

#     # --------------------------------------------------
#     # TREND STRENGTH
#     # --------------------------------------------------

#     adx = ta.trend.ADXIndicator(
#         high=high, low=low, close=close, window=14
#     )
#     df["ADX"]    = adx.adx()
#     df["DI_POS"] = adx.adx_pos()   # +DI
#     df["DI_NEG"] = adx.adx_neg()   # −DI

#     # --------------------------------------------------
#     # VOLUME
#     # --------------------------------------------------

#     df["OBV"] = ta.volume.on_balance_volume(
#         close=close, volume=vol
#     )

#     # Rolling 20-bar average volume
#     df["VOL_AVG20"] = vol.rolling(window=20).mean()

#     # Relative Volume  (1.0 = exactly average)
#     df["REL_VOL"] = vol / df["VOL_AVG20"]

#     # --------------------------------------------------
#     # SUPPORT & RESISTANCE via swing pivots  (new)
#     # --------------------------------------------------
#     #
#     # A swing high is a bar whose high is higher than the
#     # N bars on either side.  N=5 gives a good balance
#     # between sensitivity and noise on daily data.
#     #
#     # We look back over the last 60 bars so that the
#     # levels are recent and actionable.

#     WINDOW   = 5     # pivot look-back/look-forward
#     LOOKBACK = 60    # how many bars to search

#     df["SWING_HIGH"] = _swing_highs(high, WINDOW)
#     df["SWING_LOW"]  = _swing_lows(low,  WINDOW)

#     # Most-recent swing high → resistance
#     # Most-recent swing low  → support
#     recent_highs = (
#         df["SWING_HIGH"]
#         .dropna()
#         .tail(LOOKBACK)
#     )
#     recent_lows = (
#         df["SWING_LOW"]
#         .dropna()
#         .tail(LOOKBACK)
#     )

#     df.attrs["RESISTANCE"] = (
#         float(recent_highs.iloc[-1])
#         if not recent_highs.empty
#         else float(df["High"].tail(LOOKBACK).max())
#     )

#     df.attrs["SUPPORT"] = (
#         float(recent_lows.iloc[-1])
#         if not recent_lows.empty
#         else float(df["Low"].tail(LOOKBACK).min())
#     )

#     return df


# # ------------------------------------------------------
# # PRIVATE HELPERS
# # ------------------------------------------------------

# def _swing_highs(high_series, window: int):
#     """
#     Return a Series that contains the swing-high price
#     at its bar index and NaN everywhere else.
#     """
#     arr = high_series.values
#     n   = len(arr)
#     out = np.full(n, np.nan)

#     for i in range(window, n - window):
#         segment = arr[i - window: i + window + 1]
#         if arr[i] == segment.max():
#             out[i] = arr[i]

#     return type(high_series)(
#         out, index=high_series.index
#     )


# def _swing_lows(low_series, window: int):
#     """
#     Return a Series that contains the swing-low price
#     at its bar index and NaN everywhere else.
#     """
#     arr = low_series.values
#     n   = len(arr)
#     out = np.full(n, np.nan)

#     for i in range(window, n - window):
#         segment = arr[i - window: i + window + 1]
#         if arr[i] == segment.min():
#             out[i] = arr[i]

#     return type(low_series)(
#         out, index=low_series.index
#     )

# # import ta


# # def calculate_indicators(df):

# #     # EMA
# #     df["EMA20"] = ta.trend.ema_indicator(
# #         df["Close"],
# #         window=20
# #     )

# #     df["EMA50"] = ta.trend.ema_indicator(
# #         df["Close"],
# #         window=50
# #     )

# #     # RSI
# #     df["RSI"] = ta.momentum.rsi(
# #         df["Close"],
# #         window=14
# #     )

# #     # MACD
# #     macd = ta.trend.MACD(df["Close"])

# #     df["MACD"] = macd.macd()
# #     df["MACD_SIGNAL"] = macd.macd_signal()
# #     df["MACD_HIST"] = macd.macd_diff()

# #     # Bollinger Bands
# #     bb = ta.volatility.BollingerBands(
# #         df["Close"],
# #         window=20,
# #         window_dev=2
# #     )

# #     df["BB_UPPER"] = bb.bollinger_hband()
# #     df["BB_MIDDLE"] = bb.bollinger_mavg()
# #     df["BB_LOWER"] = bb.bollinger_lband()

# #     # ATR
# #     atr = ta.volatility.AverageTrueRange(
# #         high=df["High"],
# #         low=df["Low"],
# #         close=df["Close"],
# #         window=14
# #     )

# #     df["ATR"] = atr.average_true_range()

# #     # ADX
# #     adx = ta.trend.ADXIndicator(
# #         high=df["High"],
# #         low=df["Low"],
# #         close=df["Close"],
# #         window=14
# #     )

# #     df["ADX"] = adx.adx()

# #     # OBV
# #     df["OBV"] = ta.volume.on_balance_volume(
# #         close=df["Close"],
# #         volume=df["Volume"]
# #     )

# #     return df
