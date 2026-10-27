import requests

PRICE_URL = (
    "https://s3.eu-west-2.amazonaws.com/"
    "game-assets.fut.gg/27/cdn-data/player-prices-ps5.json"
)

def fetch_futgg_prices():
    response = requests.get(PRICE_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    player_id = data["id0"]
    prices = {}

    for index, price in enumerate(data["p"]):
        if index > 0:
            player_id += data["d"][index - 1]

        if price > 0:
            prices[player_id] = price

    return prices
