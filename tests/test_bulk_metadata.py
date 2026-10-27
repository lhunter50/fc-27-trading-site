import csv
import io
import requests

from test_futgg_feed import fetch_prices

CSV_URL = (
    "https://raw.githubusercontent.com/"
    "LakshmiKanth11/EA_FC_ANALYSIS/main/"
    "EA_FC_PLAYERS_DATASET_AND_%20DASHBOARD/data/players.csv"
)


def main():
    prices = fetch_prices()

    affordable_ids = {
        ea_id
        for ea_id, price in prices.items()
        if 1_000 <= price <= 100_000
    }

    response = requests.get(CSV_URL, timeout=30)
    response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))

    print("CSV columns:", reader.fieldnames)

    metadata = {}

    for row in reader:
        player_id = row.get("player_id")

        if not player_id:
            continue

        metadata[int(player_id)] = row

    matched = affordable_ids & metadata.keys()
    missing = affordable_ids - metadata.keys()

    print(f"\nMetadata records: {len(metadata):,}")
    print(f"Affordable cards: {len(affordable_ids):,}")
    print(f"Matched cards: {len(matched):,}")
    print(f"Missing cards: {len(missing):,}")
    print(f"Coverage: {len(matched) / len(affordable_ids) * 100:.1f}%")

    print("\nSample matches:")

    for ea_id in sorted(matched)[:10]:
        player = metadata[ea_id]

        name = (
            player.get("common_name")
            or f"{player.get('first_name', '')} "
               f"{player.get('last_name', '')}"
        ).strip()

        print(f"{name} | {prices[ea_id]:,} coins")


if __name__ == "__main__":
    main()