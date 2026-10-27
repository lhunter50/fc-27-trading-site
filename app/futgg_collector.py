import sqlite3
from datetime import datetime, timezone
import time

from app.database import (
    DATABASE,
    initialize_futgg_tables,
    save_futgg_players,
    save_futgg_prices,
    initialize_futgg_freshness,
    update_futgg_last_seen,
)
from app.futgg_market import fetch_futgg_market


def collect_futgg_prices():
    initialize_futgg_tables()
    initialize_futgg_freshness()

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
    update_futgg_last_seen(players, recorded_at)
    saved_prices = save_futgg_prices(changed_players, recorded_at)

    print(f"Players received: {len(players):,}")
    print(f"Price changes/new players: {len(changed_players):,}")
    print(f"Price observations saved: {saved_prices:,}")


def run_collector_loop(interval_seconds):
    while True:
        try:
            collect_futgg_prices()
        except Exception as e:
            print(f"Error during collection: {e}")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_collector_loop(interval_seconds=900)