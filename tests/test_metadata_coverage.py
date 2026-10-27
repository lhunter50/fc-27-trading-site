import requests
from test_futgg_feed import fetch_prices

METADATA_URL = "https://www.fut.gg/api/fut/players/v2/27/"


def main():
    prices = fetch_prices()

    affordable_ids = {
        ea_id
        for ea_id, price in prices.items()
        if 1_000 <= price <= 100_000
    }

    matched = set()

    for page in range(1, 4):
        response = requests.get(
            METADATA_URL,
            params={"page": page},
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        players = data.get("data", [])

        page_matches = 0

        for player in players:
            ea_id = player.get("eaId")

            if ea_id in affordable_ids:
                matched.add(ea_id)
                page_matches += 1

                print(
                    f"{player.get('commonName')} "
                    f"| Rating: {player.get('overall')} "
                    f"| Price: {prices[ea_id]:,}"
                )

        print(
            f"Page {page}: "
            f"{len(players)} players, "
            f"{page_matches} affordable matches"
        )

    print(f"\nAffordable cards in price feed: {len(affordable_ids)}")
    print(f"Matched across 3 metadata pages: {len(matched)}")


if __name__ == "__main__":
    main()