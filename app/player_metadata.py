import csv
import io

import requests

METADATA_URL = (
    "https://raw.githubusercontent.com/"
    "LakshmiKanth11/EA_FC_ANALYSIS/main/"
    "EA_FC_PLAYERS_DATASET_AND_%20DASHBOARD/data/players.csv"
)


def fetch_player_metadata():
    response = requests.get(METADATA_URL, timeout=30)
    response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))

    players = {}

    for row in reader:
        player_id = row.get("player_id")

        if not player_id:
            continue

        ea_id = int(player_id)

        name = (
            row.get("common_name")
            or f"{row.get('first_name', '')} {row.get('last_name', '')}"
        ).strip()

        players[ea_id] = {
            "eaId": ea_id,
            "name": name,
            "rating": int(row["overall_rating"]),
            "position": row.get("position"),
            "club": row.get("club"),
            "league": row.get("league"),
        }

    return players