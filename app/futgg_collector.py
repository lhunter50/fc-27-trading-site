import sqlite3
from datetime import datetime, timezone

from app.database import (
    DATABASE,
    initialize_futgg_tables,
    save_futgg_players,
    save_futgg_prices,
)
from app.futgg_market import fetch_futgg_market


def collect_futgg_prices():
    initialize_futgg_tables()

    players = fetch_futgg_market()

    if not players:
        print("No players received. Skipping collection.")
        return

    with sqlite3.connect(DATABASE) as conn:
        previous_prices = dict(
            conn.execute("""
                SELECT h.player_id, h.price
                FROM futgg_price_history h
                WHERE h.id = (
                    SELECT MAX(h2.id)
                    FROM futgg_price_history h2
                    WHERE h2.player_id = h.player_id
                )
            """)
        )

    changed_players = [
        player
        for player in players
        if previous_prices.get(player["eaId"]) != player["price"]
    ]

    recorded_at = datetime.now(timezone.utc).isoformat()

    save_futgg_players(players)
    saved_prices = save_futgg_prices(changed_players, recorded_at)

    print(f"Players received: {len(players):,}")
    print(f"Price changes/new players: {len(changed_players):,}")
    print(f"Price observations saved: {saved_prices:,}")


if __name__ == "__main__":
    collect_futgg_prices()