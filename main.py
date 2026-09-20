import numpy as np
import yfinance as yf # use to fatch real time price of the stock
import matplotlib.pyplot as plt

ticker = input("Enter stock symbol: ")
stock = yf.Ticker(ticker)
data = stock.history(period="1y")

# Convert columns into NumPy arrays
open_price = data["Open"].to_numpy()
high_price = data["High"].to_numpy()
low_price = data["Low"].to_numpy()
close_price = data["Close"].to_numpy()
volume = data["Volume"].to_numpy()

print("\nSTOCK :-", ticker)
print("trading days:", close_price.size)

print("\n ---- FIRST 5 CLOSING PRICES ----")
print(close_price[:6])

print("\n ---- LAST 5 CLOSING PRICES ----")
print(close_price[-6:])

# price statistics
avg_price = np.mean(close_price)
median_price = np.median(close_price)
highest_price = np.max(close_price)
lowest_price = np.min(close_price)
price_std = np.std(close_price)

print("\n---------- PRICE STATISTICS ------------")

print(f"Average Price : {avg_price:.2f}")
print(f"Median Price  : {median_price:.2f}")
print(f"Highest Price : {highest_price:.2f}")
print(f"Lowest Price  : {lowest_price:.2f}")
print(f"Std Deviation : {price_std:.2f}")

# highest and lowest trading date

# highest and lowest index
highest_index = np.argmax(close_price)
lowest_index = np.argmin(close_price)

# highest and lowest date
highest_date = data.index[highest_index]
lowest_date = data.index[lowest_index]

print("\n--------- EXTREME DAYS ----------")

print("Highest Price Date:", highest_date)
print("Lowest Price Date :", lowest_date)

# daily returns

daily_returns = ((close_price[1:] - close_price[:-1]) / close_price[:-1]) * 100
# include 2nd to last price - include first to 2nd last price

# yesterday close = ₹100
# today close     = ₹105
# return = (105 - 100) / 100 × 100 = 5%

print("\n--------- DAILY RETURNS --------")
print("First 10 Daily Returns:")
print(daily_returns[:10])

# positive and negative days
positive_days = daily_returns[daily_returns > 0]
negative_days = daily_returns[daily_returns < 0]

print("\nPositive Days:", len(positive_days))
print("Negative Days:", len(negative_days))

# best and worst daily returns
print("Best Daily Return :", np.max(daily_returns))
print("Worst Daily Return:", np.min(daily_returns))

# avg daily return
avg_return = np.mean(daily_returns)
print("Average Daily Return:", f"{avg_return:.2f}%")

# volatility and risk analysis
volatility = np.std(daily_returns)

print("\n--------- RISK ANALYSIS ---------")

print(f"Daily Volatility : {volatility:.2f}%")

# Annualized Volatility
annual_volatility = volatility * np.sqrt(252)

print(f"Annualized Volatility : {annual_volatility:.2f}%")

# risk classification
if annual_volatility < 25:
    risk = "LOW"
elif annual_volatility < 42:
    risk = "MEDIUM"
else:
    risk = "HIGH"

print("Risk Level:", risk)

# downside risk
downside_volatility = np.std(negative_days)

print(f"Downside Volatility : {downside_volatility:.2f}%")

print("\n--------- DOWNSIDE RISK ANALYSIS ---------")

print(f"Daily Volatility      : {volatility:.2f}%")
print(f"Annualized Volatility : {annual_volatility:.2f}%")
print(f"Downside Volatility   : {downside_volatility:.2f}%")
print(f"Risk Level            : {risk}")

# Simple Moving Average (SMA) :- it show short term stock price very smooth
# moving avg

window = 20

moving_average = np.convolve(
    close_price,
    np.ones(window) / window,
    mode="valid"
)

print("\n---------MOVING AVERAGE ----------")
print(f"{window}-Day SMA:")
print(moving_average[-5:])

# current price vs moving average
current_price = close_price[-1]
current_sma = moving_average[-1]

print("\nCurrent Price:", current_price)
print("20-Day SMA:", current_sma)

if current_price > current_sma:
    trend = "UPTREND"
else:
    trend = "DOWNTREND"

print("Trend:", trend)

# 20-Day + 50-Day SMA

sma_20 = np.convolve(
    close_price,
    np.ones(20) / 20,
    mode="valid"
)

sma_50 = np.convolve(
    close_price,
    np.ones(50) / 50,
    mode="valid"
)

print("\n--------- TREND ANALYSIS ---------")
print("20-Day SMA:", sma_20[-1])
print("50-Day SMA:", sma_50[-1])

if sma_20[-1] > sma_50[-1]:
    trend = "BULLISH"
else:
    trend = "BEARISH"

print("Trend:", trend)

# PERFORMANCE ANALYSIS

initial_price = close_price[0]
final_price = close_price[-1]

total_return = (
    (final_price - initial_price)
    / initial_price
) * 100

print("\n------- PERFORMANCE --------")

print(f"Initial Price : {initial_price:.2f}")
print(f"Final Price   : {final_price:.2f}")
print(f"Total Return  : {total_return:.2f}%")

# best and worst trading days

best_return = np.max(daily_returns)
worst_return = np.min(daily_returns)

best_day_index = np.argmax(daily_returns)
worst_day_index = np.argmin(daily_returns)

best_day = data.index[best_day_index + 1]
worst_day = data.index[worst_day_index + 1]

print("\n-------- BEST /WORST DAYS -------")

print(f"Best Day  : {best_day} ({best_return:.2f}%)")
print(f"Worst Day : {worst_day} ({worst_return:.2f}%)")

# max drawdown

# Running maximum price
running_max = np.maximum.accumulate(close_price)

# Drawdown percentage
drawdown = (
    (close_price - running_max)
    / running_max
) * 100

max_drawdown = np.min(drawdown)

print("\n-------- DRAWDOWN -------")
print(f"Maximum Drawdown : {max_drawdown:.2f}%")

# Prices:
# 100  → 110 → 105 → 120 → 115
# Running maximum:
# 100  → 110 → 110 → 120 → 120

# VOLUME ANALYSIS

average_volume = np.mean(volume)
highest_volume = np.max(volume)
lowest_volume = np.min(volume)

print("\n--------- VOLUME ANALYSIS --------")

print(f"Average Volume : {average_volume:.0f}")
print(f"Highest Volume : {highest_volume:.0f}")
print(f"Lowest Volume  : {lowest_volume:.0f}")

# Highest volume day

highest_volume_index = np.argmax(volume)

print("\nHighest Volume Day:")

print("Date  :", data.index[highest_volume_index])
print("Volume:", volume[highest_volume_index])

# Volume spikes

volume_threshold = average_volume * 2

volume_spikes = volume[volume > volume_threshold]

print("\nVolume Spikes:", len(volume_spikes))

# Price-volume correlation

daily_volume = volume[1:]

correlation = np.corrcoef(
    daily_returns,
    daily_volume
)[0, 1]

print("\n-------- PRICE-VOLUME RELATIONSHIP --------")

print(f"Correlation: {correlation:.2f}")

# Volume signals

volume_signal = np.where(
    volume > average_volume * 2,
    "SPIKE",
    "NORMAL"
)

print("\nLast 10 Volume Signals:")
print(volume_signal[-10:])


# multiple stock comparision & ranking

print("\n--------- MULTIPLE STOCK COMPARISON ----------")

# Take multiple stocks

tickers = input(
    "Enter stock tickers (comma separated): "
).split(",")

tickers = [ticker.strip().upper() for ticker in tickers]

all_returns = []
all_total_returns = []
valid_tickers = []

# Fetch data for every stock

for ticker in tickers:

    stock = yf.Ticker(ticker)
    data_stock = stock.history(period="1y")

    if data_stock.empty:
        print(f"No data found for {ticker}")
        continue

    close = data_stock["Close"].to_numpy()

    # Daily returns

    returns = (
        (close[1:] - close[:-1])
        / close[:-1]
    ) * 100

    # Total return

    total_return = (
        (close[-1] - close[0])
        / close[0]
    ) * 100

    all_returns.append(returns)
    all_total_returns.append(total_return)
    valid_tickers.append(ticker)


# Make all arrays same length

min_length = min(
    len(returns)
    for returns in all_returns
)

all_returns = [
    returns[-min_length:]
    for returns in all_returns
]

# Convert to 2D NumPy array

returns_matrix = np.array(all_returns)

print("\nReturns Matrix Shape:")
print(returns_matrix.shape)

# Average daily return

average_returns = np.mean(
    returns_matrix,
    axis=1
)

# Volatility

volatilities = np.std(
    returns_matrix,
    axis=1
)

# Convert total returns to NumPy array

total_returns = np.array(
    all_total_returns
)

# Ranking

ranking_indices = np.argsort(
    total_returns
)[::-1]

# Display results

print("\n--------- STOCK RANKING --------")

print(
    f"{'Rank':<6}"
    f"{'Stock':<15}"
    f"{'Total Return':<18}"
    f"{'Avg Daily Return':<20}"
    f"{'Volatility':<15}"
)

print("-" * 74)

for rank, index in enumerate(
    ranking_indices,
    start=1
):

    print(
        f"{rank:<6}"
        f"{valid_tickers[index]:<15}"
        f"{total_returns[index]:>10.2f}%"
        f"{average_returns[index]:>18.4f}%"
        f"{volatilities[index]:>13.2f}%"
    )


# technical analysis

# 1. RSI - Relative Strength Index

price_change = close_price[1:] - close_price[:-1]

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

rsi_period = 14

average_gain = np.convolve(
    gains,
    np.ones(rsi_period) / rsi_period,
    mode="valid"
)

average_loss = np.convolve(
    losses,
    np.ones(rsi_period) / rsi_period,
    mode="valid"
)

# Avoid division by zero

rs = average_gain / (
    average_loss + 1e-10
)

rsi = 100 - (
    100 / (1 + rs)
)

current_rsi = rsi[-1]

# RSI Signal

if current_rsi > 70:
    rsi_signal = "OVERBOUGHT"

elif current_rsi < 30:
    rsi_signal = "OVERSOLD"

else:
    rsi_signal = "NEUTRAL"


# 2. Bollinger Bands

bb_window = 20

# Middle Band = 20-Day SMA

middle_band = np.convolve(
    close_price,
    np.ones(bb_window) / bb_window,
    mode="valid"
)

# Create rolling windows

windows = np.lib.stride_tricks.sliding_window_view(
    close_price,
    bb_window
)

# Standard deviation of every window

rolling_std = np.std(
    windows,
    axis=1
)

# Upper and Lower Bands

upper_band = (
    middle_band
    + 2 * rolling_std
)

lower_band = (
    middle_band
    - 2 * rolling_std
)

# Bollinger Signal

current_price = close_price[-1]

if current_price > upper_band[-1]:

    bb_signal = "ABOVE UPPER BAND"

elif current_price < lower_band[-1]:

    bb_signal = "BELOW LOWER BAND"

else:

    bb_signal = "INSIDE BANDS"


# 3. EMA - Exponential Moving Average

ema_period = 20

alpha = 2 / (ema_period + 1)

ema = np.zeros(
    len(close_price)
)

# First EMA value

ema[0] = close_price[0]

# Calculate remaining EMA values

for i in range(1, len(close_price)):

    ema[i] = (
        alpha * close_price[i]
        + (1 - alpha) * ema[i - 1]
    )

current_ema = ema[-1]


# EMA Signal

if current_price > current_ema:

    ema_signal = "BULLISH"

else:

    ema_signal = "BEARISH"


# FINAL TECHNICAL ANALYSIS

print("\n")

print("=" * 55)

print("              TECHNICAL ANALYSIS")

print("=" * 55)

print(f"\nStock         : {ticker}")
print(f"Current Price : {current_price:.2f}")

print("\n---------- RSI ----------")

print(f"RSI           : {current_rsi:.2f}")
print(f"RSI Signal    : {rsi_signal}")

print("\n---------- EMA ----------")

print(f"20-Day EMA    : {current_ema:.2f}")
print(f"EMA Signal    : {ema_signal}")

print("\n------ Bollinger Bands ------")

print(f"Upper Band    : {upper_band[-1]:.2f}")
print(f"Middle Band   : {middle_band[-1]:.2f}")
print(f"Lower Band    : {lower_band[-1]:.2f}")
print(f"BB Signal     : {bb_signal}")

print("\n" + "=" * 55)


# ============================================================
# STEP 11 - VISUALIZATION
# ============================================================

# 1. Closing Price Chart

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


# 2. Closing Price + SMA

plt.figure(figsize=(12, 6))

plt.plot(
    data.index,
    close_price,
    label="Closing Price"
)

# SMA 20 ke dates

sma_20_dates = data.index[19:]

plt.plot(
    sma_20_dates,
    sma_20,
    label="20-Day SMA"
)

# SMA 50 ke dates

sma_50_dates = data.index[49:]

plt.plot(
    sma_50_dates,
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


# 3. Volume Chart

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


# 4. RSI Chart

# RSI starts after the initial calculation period

rsi_dates = data.index[15:]

plt.figure(figsize=(12, 5))

plt.plot(
    rsi_dates,
    rsi,
    label="RSI"
)

plt.axhline(
    70,
    linestyle="--",
    label="Overbought (70)"
)

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


# 5. Bollinger Bands

bb_dates = data.index[19:]

plt.figure(figsize=(12, 6))

plt.plot(
    bb_dates,
    close_price[19:],
    label="Closing Price"
)

plt.plot(
    bb_dates,
    middle_band,
    label="Middle Band"
)

plt.plot(
    bb_dates,
    upper_band,
    label="Upper Band"
)

plt.plot(
    bb_dates,
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

