import numpy as np
import yfinance as yf # use to fatch real time price of the stock
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

daily_returns = ((close_price[1:] - close_price[:-1])/ close_price[:-1])*100
        # include 2nd to last price - include first to 2nd last price

#yesterday close = ₹100
#today close     = ₹105
#return = (105 - 100) / 100 × 100 = 5%

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
#Annualized Volatility
annual_volatility = volatility * np.sqrt(252)
print(f"Annualized Volatility : {annual_volatility:.2f}%")

#risk classification
if annual_volatility < 25:
    risk = "LOW"
elif annual_volatility < 42:
    risk = "MEDIUM"
else:
    risk = "HIGH"

print("Risk Level:", risk)

#downside risk
downside_volatility = np.std(negative_days)
print(f"Downside Volatility : {downside_volatility:.2f}%")

print("\n---------RISK ANALYSIS ---------")

print(f"Daily Volatility      : {volatility:.2f}%")
print(f"Annualized Volatility : {annual_volatility:.2f}%")
print(f"Downside Volatility   : {downside_volatility:.2f}%")
print(f"Risk Level            : {risk}")

# Simple Moving Average (SMA) :- it show short term stock price very smooth
#moving avg

window = 20
moving_average = np.convolve(
    close_price,
    np.ones(window) / window,
    mode="valid"
)
print("\n---------MOVING AVERAGE ----------")

print(f"{window}-Day SMA:")
print(moving_average[-5:])

#current price vs moving average
current_price = close_price[-1]
current_sma = moving_average[-1]

print("\nCurrent Price:", current_price)
print("20-Day SMA:", current_sma)

if current_price > current_sma:
    trend = "UPTREND"
else:
    trend = "DOWNTREND"

print("Trend:", trend)

#20-Day + 50-Day SMA
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





































