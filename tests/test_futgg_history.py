import sqlite3

from app.database import DATABASE


def main():
    with sqlite3.connect(DATABASE) as conn:
        players = conn.execute(
            "SELECT COUNT(*) FROM futgg_players"
        ).fetchone()[0]

        observations = conn.execute(
            "SELECT COUNT(*) FROM futgg_price_history"
        ).fetchone()[0]

        players_with_history = conn.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT player_id
                FROM futgg_price_history
                GROUP BY player_id
                HAVING COUNT(*) >= 2
            )
        """).fetchone()[0]

        latest = conn.execute("""
            SELECT MAX(recorded_at)
            FROM futgg_price_history
        """).fetchone()[0]

    print(f"Total players: {players:,}")
    print(f"Total price observations: {observations:,}")
    print(f"Players with 2+ observations: {players_with_history:,}")
    print(f"Latest saved price change: {latest}")


if __name__ == "__main__":
    main()