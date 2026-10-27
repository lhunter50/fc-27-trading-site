import requests

URL = (
    "https://s3.eu-west-2.amazonaws.com/"
    "game-assets.fut.gg/27/cdn-data/player-prices-ps5.json"
)


def fetch_prices():
    response = requests.get(URL, timeout=30)
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


def main():
    prices = fetch_prices()

    budget = {
        player_id: price
        for player_id, price in prices.items()
        if 1_000 <= price <= 10_000
    }

    mid_range = {
        player_id: price
        for player_id, price in prices.items()
        if 10_000 < price <= 100_000
    }

    print(f"Total priced players: {len(prices):,}")
    print(f"Budget players: {len(budget):,}")
    print(f"Mid-range players: {len(mid_range):,}")
    print(f"Total affordable players: {len(budget) + len(mid_range):,}")

    print("\nSample player IDs and prices:")

    for player_id, price in list(budget.items())[:10]:
        print(f"{player_id}: {price:,} coins")


if __name__ == "__main__":
    main()