
import requests

API_URL = "https://fc27-market.val.run/latest"


def get_market_prices():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()

    data = response.json()
    updated_at = data.get("updated")

    if not updated_at:
        raise ValueError("Market API did not provide an update timestamp")

    players = []

    for category, player_list in data.get("groups", {}).items():
        for player in player_list:
            players.append({
                **player,
                "category": category
            })

    return players, updated_at
