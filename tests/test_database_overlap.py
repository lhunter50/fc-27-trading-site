import sqlite3

from app.database import DATABASE
from app.futgg_market import fetch_futgg_market


def main():
    players = fetch_futgg_market()
    new_ids = {player["eaId"] for player in players}

    with sqlite3.connect(DATABASE) as conn:
        existing_ids = {
            row[0]
            for row in conn.execute(
                "SELECT ea_id FROM players"
            )
        }

    overlapping = new_ids & existing_ids
    new_only = new_ids - existing_ids

    print(f"Existing database players: {len(existing_ids):,}")
    print(f"New feed players: {len(new_ids):,}")
    print(f"Already in database: {len(overlapping):,}")
    print(f"New players to add: {len(new_only):,}")


if __name__ == "__main__":
    main()