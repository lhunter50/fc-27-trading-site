from app.futgg_prices import fetch_futgg_prices
from app.player_metadata import fetch_player_metadata


def fetch_futgg_market():
    prices = fetch_futgg_prices()
    metadata = fetch_player_metadata()

    players = []

    for ea_id, price in prices.items():
        if not 1_000 <= price <= 100_000:
            continue

        player = metadata.get(ea_id)

        if player is None:
            continue

        category = "budget" if price <= 10_000 else "mid_range"

        players.append({
            "eaId": ea_id,
            "name": player["name"],
            "rating": player["rating"],
            "price": price,
            "category": category,
            "rarityId": None,
            "image": None,
        })

    return players