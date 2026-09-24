import matplotlib.pyplot as plt

# 1. CLOSING PRICE CHART

def plot_closing_price(data, close_price, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(
        data.index,
        close_price,
        label="Closing Price"
    )

    plt.title(f"{ticker} - Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 2. PRICE + MOVING AVERAGES

def plot_moving_averages(
    data,
    close_price,
    sma_20,
    sma_50,
    ticker
):

    plt.figure(figsize=(12, 6))

    # Closing Price
    plt.plot(
        data.index,
        close_price,
        label="Closing Price"
    )

    # 20 Day SMA
    plt.plot(
        data.index[19:],
        sma_20,
        label="20-Day SMA"
    )

    # 50 Day SMA
    plt.plot(
        data.index[49:],
        sma_50,
        label="50-Day SMA"
    )

    plt.title(
        f"{ticker} - Price & Moving Averages"
    )

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 3. TRADING VOLUME CHART

def plot_volume(data, volume, ticker):
    plt.figure(figsize=(12, 5))
    plt.bar(
        data.index,
        volume
    )

    plt.title(
        f"{ticker} - Trading Volume"
    )

    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 4. RSI CHART

def plot_rsi(data, rsi, ticker):
    plt.figure(figsize=(12, 5))

     # RSI ke according exact dates
    rsi_dates = data.index[
        len(data.index) - len(rsi):
    ]
    
    # RSI starts after 15 data points
    plt.plot(
        rsi_dates,
        rsi,
        label="RSI"
    )

    # Overbought level
    plt.axhline(
        70,
        linestyle="--",
        label="Overbought (70)"
    )

    # Oversold level
    plt.axhline(
        30,
        linestyle="--",
        label="Oversold (30)"
    )

    plt.title(
        f"{ticker} - RSI"
    )

    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 5. BOLLINGER BANDS
def plot_bollinger_bands(
    data,
    close_price,
    middle_band,
    upper_band,
    lower_band,
    ticker
):

    plt.figure(figsize=(12, 6))

    # Bollinger Bands start after 19 data points
    dates = data.index[19:]

    # Closing Price
    plt.plot(
        dates,
        close_price[19:],
        label="Closing Price"
    )

    # Middle Band
    plt.plot(
        dates,
        middle_band,
        label="Middle Band"
    )

    # Upper Band
    plt.plot(
        dates,
        upper_band,
        label="Upper Band"
    )

    # Lower Band
    plt.plot(
        dates,
        lower_band,
        label="Lower Band"
    )

    plt.title(
        f"{ticker} - Bollinger Bands"
    )

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()