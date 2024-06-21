import requests
import numpy as np
import json

def get_top_10_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return []

def format_crypto_data(crypto_data):
    formatted_data = []
    for crypto in crypto_data:
        formatted_data.append(
            f"{crypto['name']} (Symbol: {crypto['symbol'].upper()})\n"
            f"Current Price: ${crypto['current_price']}\n"
            f"Market Cap: ${crypto['market_cap']}\n"
            f"24h Change: {crypto['price_change_percentage_24h']}%\n"
            f"-----------------------------"
        )
    return "\n".join(formatted_data)

def get_historical_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = [price[1] for price in data['prices']]
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data from CoinGecko: {e}")
        return []

def calculate_moving_average(prices, window):
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window

def calculate_rsi(prices, window=14):
    if len(prices) < window + 1:
        return None
    deltas = np.diff(prices)
    seed = deltas[:window]
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:window] = 100. - 100. / (1. + rs)

    for i in range(window, len(prices)):
        delta = deltas[i - 1]  # The diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (window - 1) + upval) / window
        down = (down * (window - 1) + downval) / window

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi[-1]

def get_support_resistance(prices):
    support = min(prices)
    resistance = max(prices)
    return support, resistance

def get_buy_sell_signals(prices):
    ma_50 = calculate_moving_average(prices, 50)
    ma_100 = calculate_moving_average(prices, 100)
    rsi = calculate_rsi(prices)
    support, resistance = get_support_resistance(prices)

    if ma_50 and ma_100 and rsi is not None:
        if ma_50 > ma_100 and rsi < 30 and prices[-1] > support:
            return "Buy"
        elif ma_50 < ma_100 and rsi > 70 and prices[-1] < resistance:
            return "Sell"
    return "Hold"

def get_crypto_signals():
    top_cryptos = get_top_10_cryptos()
    signals = []
    for crypto in top_cryptos:
        coin_id = crypto['id']
        prices = get_historical_data(coin_id, 100)
        if prices:
            signal = get_buy_sell_signals(prices)
            signals.append(
                f"{crypto['name']} (Symbol: {crypto['symbol'].upper()})\n"
                f"Current Price: ${crypto['current_price']}\n"
                f"Market Cap: ${crypto['market_cap']}\n"
                f"24h Change: {crypto['price_change_percentage_24h']}%\n"
                f"Signal: {signal}\n"
                f"-----------------------------"
            )
    return "\n".join(signals)

def get_crypto_analysis(coin_id):
    prices = get_historical_data(coin_id, 100)
    if prices:
        signal = get_buy_sell_signals(prices)
        support, resistance = get_support_resistance(prices)
        rsi = calculate_rsi(prices)
        ma_50 = calculate_moving_average(prices, 50)
        ma_100 = calculate_moving_average(prices, 100)

        return (
            f"Moving Average (50 days): ${ma_50}\n"
            f"Moving Average (100 days): ${ma_100}\n"
            f"RSI: {rsi}\n"
            f"Support: ${support}\n"
            f"Resistance: ${resistance}\n"
            f"Signal: {signal}\n"
        )
    return "Error fetching data for the given cryptocurrency."


import json

# Mock functions for subscriptions, referrals, and leaderboard
def subscribe_user(user_id):
    # Implement logic to subscribe a user and accept payment via Telegram Wallet
    # This is a placeholder, replace with actual Telegram Wallet integration
    return True

def get_referral_link(user_id):
    # Implement logic to generate and retrieve a referral link for a user
    return f"https://t.me/YourBot?start=ref_{user_id}"

def register_referral(referrer_id, referred_id):
    # Implement logic to register a referral
    return True

def get_leaderboard():
    # Implement logic to retrieve the leaderboard data
    return [
        {"user_id": 1, "referrals": 10},
        {"user_id": 2, "referrals": 8},
        {"user_id": 3, "referrals": 5},
    ]

def format_leaderboard(leaderboard):
    formatted = "🏆 Leaderboard:\n\n"
    for entry in leaderboard:
        formatted += f"👤 User ID: {entry['user_id']} - 📈 Referrals: {entry['referrals']}\n"
    return formatted
