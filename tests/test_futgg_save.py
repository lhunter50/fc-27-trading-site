import sqlite3
from datetime import datetime, timezone

from app.database import (
    DATABASE,
    save_futgg_players,
    save_futgg_prices,
)
from app.futgg_market import fetch_futgg_market


def main():
    players = fetch_futgg_market()

    # Only test the first five players.
    sample = players[:5]

    recorded_at = datetime.now(timezone.utc).isoformat()

    saved_players = save_futgg_players(sample)
    saved_prices = save_futgg_prices(sample, recorded_at)

    print(f"Player records saved: {saved_players}")
    print(f"Price observations saved: {saved_prices}")

    with sqlite3.connect(DATABASE) as conn:
        player_count = conn.execute(
            "SELECT COUNT(*) FROM futgg_players"
        ).fetchone()[0]

        price_count = conn.execute(
            "SELECT COUNT(*) FROM futgg_price_history"
        ).fetchone()[0]

    print(f"Total FUT.GG players in database: {player_count}")
    print(f"Total FUT.GG price observations: {price_count}")


if __name__ == "__main__":
    main()