import numpy as np
def calculate_sma(close_price, window):
    return np.convolve(
        close_price,
        np.ones(window) / window,
        mode="valid"
    )

def calculate_rsi(close_price, period=14):
    price_change = (close_price[1:]- close_price[:-1])
    gains = np.where(
        price_change > 0,
        price_change,
        0
    )

    losses = np.where(
        price_change < 0,
        -price_change,
        0
    )

    average_gain = np.convolve(
        gains,
        np.ones(period) / period,
        mode="valid"
    )

    average_loss = np.convolve(
        losses,
        np.ones(period) / period,
        mode="valid"
    )

    rs = average_gain / (average_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_ema(close_price, period=20):
    alpha = 2 / (period + 1)
    ema = np.zeros(len(close_price))

    ema[0] = close_price[0]

    for i in range(1, len(close_price)):
        ema[i] = (
            alpha * close_price[i]
            + (1 - alpha) * ema[i - 1]
        )

    return ema

def calculate_bollinger_bands(
    close_price,
    window=20
):

    middle_band = calculate_sma(
        close_price,
        window
    )

    windows = np.lib.stride_tricks.sliding_window_view(
        close_price,
        window
    )

    rolling_std = np.std(
        windows,
        axis=1
    )

    upper_band = (middle_band+ 2 * rolling_std)
    lower_band = (middle_band- 2 * rolling_std)

    return (middle_band,upper_band,lower_band)

def get_rsi_signal(rsi):
    current_rsi = rsi[-1]

    if current_rsi > 70:
        return "OVERBOUGHT"
    elif current_rsi < 30:
        return "OVERSOLD"
    else:
        return "NEUTRAL"

def get_ema_signal(current_price,ema):

    if current_price > ema[-1]:
        return "BULLISH"

    return "BEARISH"

def get_sma_signal(sma_20,sma_50):

    if sma_20[-1] > sma_50[-1]:
        return "BULLISH"

    return "BEARISH"


def get_bollinger_signal(
    current_price,
    upper_band,
    lower_band
):

    if current_price > upper_band[-1]:
        return "ABOVE UPPER BAND"

    elif current_price < lower_band[-1]:
        return "BELOW LOWER BAND"

    else:
        return "INSIDE BANDS"