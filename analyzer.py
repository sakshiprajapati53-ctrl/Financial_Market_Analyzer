import numpy as np
def price_statistics(close_price):
    return {
        "average": np.mean(close_price),
        "median": np.median(close_price),
        "highest": np.max(close_price),
        "lowest": np.min(close_price),
        "std": np.std(close_price),
        "highest_index": np.argmax(close_price),
        "lowest_index": np.argmin(close_price)
    }


def calculate_daily_returns(close_price):
    return (
        (close_price[1:] - close_price[:-1])
        / close_price[:-1]
    ) * 100


def risk_analysis(daily_returns):
    volatility = np.std(daily_returns)
    annual_volatility = volatility * np.sqrt(252)

    negative_returns = daily_returns[daily_returns < 0]

    if len(negative_returns) > 0:
        downside_volatility = np.std(negative_returns)
    else:
        downside_volatility = 0

    if annual_volatility < 20:
        risk = "LOW"
    elif annual_volatility < 40:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "daily_volatility": volatility,
        "annual_volatility": annual_volatility,
        "downside_volatility": downside_volatility,
        "risk": risk
    }


def performance_analysis(close_price):
    initial_price = close_price[0]
    final_price = close_price[-1]
    total_return = ((final_price - initial_price)/ initial_price) * 100
    initial_investment = 10000
    final_investment = (initial_investment* final_price/ initial_price)
    profit_loss = final_investment - initial_investment

    return {
        "initial_price": initial_price,
        "final_price": final_price,
        "total_return": total_return,
        "initial_investment": initial_investment,
        "final_investment": final_investment,
        "profit_loss": profit_loss
    }


def drawdown_analysis(close_price):
    running_max = np.maximum.accumulate(close_price)

    drawdown = (
        (close_price - running_max)
        / running_max
    ) * 100

    return np.min(drawdown)


def volume_analysis(volume):
    average_volume = np.mean(volume)
    highest_volume = np.max(volume)
    lowest_volume = np.min(volume)
    highest_volume_index = np.argmax(volume)
    volume_threshold = average_volume * 2
    volume_spikes = volume[volume > volume_threshold]

    return {
        "average_volume": average_volume,
        "highest_volume": highest_volume,
        "lowest_volume": lowest_volume,
        "highest_volume_index": highest_volume_index,
        "volume_spikes": len(volume_spikes)
    }


def price_volume_correlation(daily_returns, volume):
    daily_volume = volume[1:]

    return np.corrcoef(
        daily_returns,
        daily_volume
    )[0, 1]

def stock_analysis_score(
    current_price,
    current_rsi,
    ema,
    sma_20,
    sma_50,
    total_return,
    annual_volatility,
    bb_signal
):
    score = 0
    reasons = []

    # RSI
    if current_rsi < 30:
        score += 2
        reasons.append("RSI indicates oversold condition")
    elif current_rsi > 70:
        score -= 2
        reasons.append("RSI indicates overbought condition")
    else:
        reasons.append("RSI is in neutral range")

    # EMA
    if current_price > ema[-1]:
        score += 2
        reasons.append("Price is above EMA")
    else:
        score -= 2
        reasons.append("Price is below EMA")

    # SMA
    if sma_20[-1] > sma_50[-1]:
        score += 2
        reasons.append("20-Day SMA is above 50-Day SMA")
    else:
        score -= 2
        reasons.append("20-Day SMA is below 50-Day SMA")

    # Total Return
    if total_return > 0:
        score += 1
        reasons.append("Positive 1-year return")
    else:
        score -= 1
        reasons.append("Negative 1-year return")

    # Volatility
    if annual_volatility < 20:
        score += 1
        reasons.append("Relatively lower volatility")
    elif annual_volatility > 40:
        score -= 1
        reasons.append("High volatility")
    else:
        reasons.append("Moderate volatility")

    # Bollinger Bands
    if bb_signal == "BELOW LOWER BAND":
        score += 1
        reasons.append("Price is below lower Bollinger Band")

    elif bb_signal == "ABOVE UPPER BAND":
        score -= 1
        reasons.append("Price is above upper Bollinger Band")

    else:
        reasons.append("Price is inside Bollinger Bands")

    # Final signal
    if score >= 4:
        signal = "BULLISH"
    elif score <= -4:
        signal = "BEARISH"
    else:
        signal = "NEUTRAL"

    return score, signal, reasons