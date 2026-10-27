from app.futgg_prices import fetch_futgg_prices
from app.player_metadata import fetch_player_metadata


def main():
    prices = fetch_futgg_prices()
    metadata = fetch_player_metadata()

    players = []

    for ea_id, price in prices.items():
        if not 1_000 <= price <= 100_000:
            continue

        player = metadata.get(ea_id)

        if player is None:
            continue

        players.append({
            **player,
            "price": price,
        })

    print(f"Players with metadata: {len(players):,}")

    print("\nSample players:")

    for player in players[:10]:
        print(
            f"{player['name']} "
            f"| Rating: {player['rating']} "
            f"| Price: {player['price']:,}"
        )


if __name__ == "__main__":
    main()