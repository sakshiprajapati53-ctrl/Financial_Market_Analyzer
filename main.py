import numpy as np
import yfinance as yf # use to fatch real time price of the stock
from visualizer import (plot_closing_price,plot_moving_averages,plot_volume,plot_rsi,plot_bollinger_bands)
from analyzer import (price_statistics,calculate_daily_returns,risk_analysis,performance_analysis,drawdown_analysis,volume_analysis,price_volume_correlation,stock_analysis_score)
from indicators import (calculate_sma,calculate_rsi,calculate_ema,calculate_bollinger_bands,get_rsi_signal,get_ema_signal,get_sma_signal,get_bollinger_signal)

# stock data
stock_symbol = input("Enter stock symbol: ").strip().upper()

if not stock_symbol:
    print("Stock symbol cannot be empty.")
    exit()

try:
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1y")

except Exception as e:
    print("Error while fetching stock data.")
    print("Error:", e)
    exit()

# Check data
if data.empty:
    print(f"No data found for {stock_symbol}.")
    print("Please check the stock symbol and try again.")
    exit()

# Check minimum data
if len(data) < 50:
    print(f"Insufficient data for {stock_symbol}.")
    print("At least 50 trading days are required.")
    exit()

data = data.dropna(subset=["Open", "High", "Low", "Close", "Volume"])

# Convert columns into NumPy arrays
open_price = data["Open"].to_numpy()
high_price = data["High"].to_numpy()
low_price = data["Low"].to_numpy()
close_price = data["Close"].to_numpy()
volume = data["Volume"].to_numpy()

print("trading days:", close_price.size)

print("\n ---- FIRST 5 CLOSING PRICES ----")
print(close_price[:6])

print("\n ---- LAST 5 CLOSING PRICES ----")
print(close_price[-6:])

# data validation
if np.isnan(close_price).any():
    print("Warning: Missing closing price data found.")

if np.isnan(volume).any():
    print("Warning: Missing volume data found.")

# price statistics
stats = price_statistics(close_price)

print("\n---------- PRICE STATISTICS ------------")
print(f"Average Price : {stats['average']:.2f}")
print(f"Median Price  : {stats['median']:.2f}")
print(f"Highest Price : {stats['highest']:.2f}")
print(f"Lowest Price  : {stats['lowest']:.2f}")
print(f"Std Deviation : {stats['std']:.2f}")

# highest and lowest trading date

# highest and lowest index
highest_index = stats["highest_index"]
lowest_index = stats["lowest_index"]

# highest and lowest date
highest_date = data.index[highest_index]
lowest_date = data.index[lowest_index]

print("\n--------- EXTREME DAYS ----------")

print("Highest Price Date:", highest_date)
print("Lowest Price Date :", lowest_date)

# daily returns
daily_returns = calculate_daily_returns(close_price)

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
print("\n--------- RISK ANALYSIS ---------")

risk = risk_analysis(daily_returns)

print(
    f"Daily Volatility : "
    f"{risk['daily_volatility']:.2f}%"
)

print(
    f"Annualized Volatility : "
    f"{risk['annual_volatility']:.2f}%"
)

print(
    f"Downside Volatility : "
    f"{risk['downside_volatility']:.2f}%"
)

print("Risk Level:", risk["risk"])

# Simple Moving Average (SMA) :- it show short term stock price very smooth
# moving avg

window = 20

moving_average = calculate_sma(close_price, window)

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

sma_20 = calculate_sma(close_price, 20)
sma_50 = calculate_sma(close_price, 50)

print("\n--------- TREND ANALYSIS ---------")
print("20-Day SMA:", sma_20[-1])
print("50-Day SMA:", sma_50[-1])

if sma_20[-1] > sma_50[-1]:
    trend = "BULLISH"
else:
    trend = "BEARISH"

print("Trend:", trend)

# PERFORMANCE ANALYSIS

performance = performance_analysis(close_price)

initial_price = performance["initial_price"]
final_price = performance["final_price"]

main_stock_return = performance["total_return"]

print("\n------- PERFORMANCE --------")
print(f"Initial Price : {initial_price:.2f}")
print(f"Final Price   : {final_price:.2f}")
print(f"Total Return  : {main_stock_return:.2f}%")

print(f"Initial Investment : ₹{performance['initial_investment']:.2f}")
print(f"Final Investment   : ₹{performance['final_investment']:.2f}")
print(f"Profit / Loss      : ₹{performance['profit_loss']:.2f}")

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

max_drawdown = drawdown_analysis(close_price)

print("\n-------- DRAWDOWN -------")
print(f"Maximum Drawdown : {max_drawdown:.2f}%")

# Prices:
# 100  → 110 → 105 → 120 → 115
# Running maximum:
# 100  → 110 → 110 → 120 → 120

# VOLUME ANALYSIS

volume_stats = volume_analysis(volume)

average_volume = volume_stats["average_volume"]
highest_volume = volume_stats["highest_volume"]
lowest_volume = volume_stats["lowest_volume"]

print("\n--------- VOLUME ANALYSIS --------")
print(f"Average Volume : {average_volume:.0f}")
print(f"Highest Volume : {highest_volume:.0f}")
print(f"Lowest Volume  : {lowest_volume:.0f}")

# Highest volume day

highest_volume_index = volume_stats["highest_volume_index"]

print("\nHighest Volume Day:")
print("Date  :", data.index[highest_volume_index])
print("Volume:", volume[highest_volume_index])

# Volume spikes

print("\nVolume Spikes:", volume_stats["volume_spikes"])

# Price-volume correlation

correlation = price_volume_correlation(
    daily_returns,
    volume
)

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
    try:
        stock_compare = yf.Ticker(ticker)
        data_stock = stock_compare.history(period="1y")
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        continue

# data safety
    if data_stock.empty:
        print(f"No datafound for {ticker}")
        continue

    data_stock = data_stock.dropna(subset=["Close"])

    if len(data_stock) < 2:
        print(f"Insufficient data for {ticker}")
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

# Check if valid stocks exist

if len(all_returns) == 0:
    print("No valid stocks found.")
    exit()

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
total_returns = np.array(all_total_returns)

# Ranking
ranking_indices = np.argsort(total_returns)[::-1]

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

for rank, index in enumerate(ranking_indices, start=1):
    print(
        f"{rank:<6}"
        f"{valid_tickers[index]:<15}"
        f"{total_returns[index]:>10.2f}%"
        f"{average_returns[index]:>18.4f}%"
        f"{volatilities[index]:>13.2f}%"
    )


# technical analysis

# 1. RSI - Relative Strength Index
rsi = calculate_rsi(close_price)
current_rsi = rsi[-1]

# RSI Signal
rsi_signal = get_rsi_signal(rsi)

# 2. Bollinger Bands
bb_window = 20

# Middle Band = 20-Day SMA
middle_band, upper_band, lower_band = calculate_bollinger_bands(close_price,bb_window)

# Create rolling windows
# Standard deviation of every window
# Upper and Lower Bands
# Bollinger Signal

current_price = close_price[-1]
bb_signal = get_bollinger_signal(current_price,upper_band,lower_band)

# 3. EMA - Exponential Moving Average
ema_period = 20
ema = calculate_ema(close_price,ema_period)
current_ema = ema[-1]

# EMA Signal
ema_signal = get_ema_signal(current_price,ema)

# FINAL TECHNICAL ANALYSIS

print("=" * 55)
print("------------TECHNICAL ANALYSIS -----------")
print("=" * 55)

print(f"\nStock         : {stock_symbol}")
print(f"Current Price : {current_price:.2f}")

print("\n---------- RSI ----------")
print(f"RSI           : {current_rsi:.2f}")
print(f"RSI Signal    : {rsi_signal}")

print("\n---------- SMA ----------")
print(f"20-Day SMA    : {sma_20[-1]:.2f}")
print(f"50-Day SMA    : {sma_50[-1]:.2f}")

sma_signal = get_sma_signal(
    sma_20,
    sma_50
)

print(f"SMA Signal    : {sma_signal}")

print("\n---------- EMA ----------")
print(f"20-Day EMA    : {current_ema:.2f}")
print(f"EMA Signal    : {ema_signal}")

print("\n------ Bollinger Bands ------")
print(f"Upper Band    : {upper_band[-1]:.2f}")
print(f"Middle Band   : {middle_band[-1]:.2f}")
print(f"Lower Band    : {lower_band[-1]:.2f}")
print(f"BB Signal     : {bb_signal}")

print("\n" + "=" * 55)

# VISUALIZATION

plot_closing_price(data,close_price,stock_symbol)
plot_moving_averages(data,close_price,sma_20,sma_50,stock_symbol)
plot_volume(data,volume,stock_symbol)
plot_rsi(data,rsi,stock_symbol)
plot_bollinger_bands(data,close_price,middle_band,upper_band,lower_band,stock_symbol)

# FINAL STOCK ANALYSIS
# function calls --> of analyzer.py
score, suggestion, reasons = stock_analysis_score(
    current_price,
    current_rsi,
    ema,
    sma_20,
    sma_50,
    main_stock_return,
    risk["annual_volatility"],
    bb_signal
)

print("------FINAL STOCK ANALYSIS------")
print("Stock         :", stock_symbol)
print("Analysis Score:", score)
print("Overall Signal:", suggestion)
print("\nReasons:")

for reason in reasons:
    print("-", reason)