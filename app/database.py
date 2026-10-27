
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DATABASE = Path(__file__).resolve().parent.parent / "data" / "market.db"

def initialize_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                rating INTEGER,
                category TEXT,
                price INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                UNIQUE(player_id, recorded_at)
            )
        """)


def initialize_futgg_tables():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS futgg_players (
                ea_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                rating INTEGER,
                category TEXT,
                image_url TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS futgg_price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                price INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                UNIQUE(player_id, recorded_at)
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_futgg_history_player_time
            ON futgg_price_history(player_id, recorded_at)
        """)

def initialize_futgg_freshness():
    with sqlite3.connect(DATABASE) as conn:
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(futgg_players)")
        }
        if "last_seen_at" not in columns:
            conn.execute("""
                ALTER TABLE futgg_players
                ADD COLUMN last_seen_at TEXT
            """)

def update_futgg_last_seen(players, recorded_at):
    player_ids = [player["eaId"] for player in players]

    with sqlite3.connect(DATABASE) as conn:
        conn.executemany("""
            UPDATE futgg_players
            SET last_seen_at = ?
            WHERE ea_id = ?
        """, [(recorded_at, player_id) for player_id in player_ids])

def save_futgg_players(players):
    saved = 0

    with sqlite3.connect(DATABASE) as conn:
        for player in players:
            cursor = conn.execute("""
                INSERT INTO futgg_players (
                    ea_id, name, rating, category, image_url
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(ea_id) DO UPDATE SET
                    name = excluded.name,
                    rating = excluded.rating,
                    category = excluded.category,
                    image_url = COALESCE(
                        excluded.image_url,
                        futgg_players.image_url
                    )
            """, (
                player["eaId"],
                player["name"],
                player.get("rating"),
                player.get("category"),
                player.get("image")
            ))

            saved += cursor.rowcount

    return saved


def save_futgg_prices(players, recorded_at):
    saved = 0

    with sqlite3.connect(DATABASE) as conn:
        for player in players:
            player_id = player.get("eaId")
            price = player.get("price")

            if (
                not isinstance(player_id, int)
                or not isinstance(price, int)
                or price <= 0
            ):
                continue

            cursor = conn.execute("""
                INSERT OR IGNORE INTO futgg_price_history (
                    player_id, price, recorded_at
                )
                VALUES (?, ?, ?)
            """, (
                player_id,
                price,
                recorded_at
            ))

            saved += cursor.rowcount

    return saved

def save_prices(players, recorded_at):
    saved = 0

    with sqlite3.connect(DATABASE) as conn:
        for player in players:
            player_id = player.get("eaId")
            price = player.get("price")

            if player_id is None or not isinstance(price, int) or price <= 0:
                continue

            cursor = conn.execute("""
                INSERT OR IGNORE INTO price_history
                (player_id, name, rating, category, price, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                player_id,
                player.get("name"),
                player.get("rating"),
                player.get("category"),
                price,
                recorded_at
            ))

            saved += cursor.rowcount

    return saved


def initialize_players_table():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                ea_id INTEGER PRIMARY KEY,
                name TEXT,
                rating INTEGER,
                rarity_id INTEGER,
                category TEXT,
                image_url TEXT
            )
        """)


def save_players(players):
    saved = 0

    with sqlite3.connect(DATABASE) as conn:
        for player in players:
            cursor = conn.execute("""
                INSERT INTO players (
                    ea_id, name, rating, rarity_id,
                    category, image_url
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(ea_id) DO UPDATE SET
                    name = excluded.name,
                    rating = excluded.rating,
                    rarity_id = excluded.rarity_id,
                    category = excluded.category,
                    image_url = excluded.image_url
            """, (
                player["eaId"],
                player.get("name"),
                player.get("rating"),
                player.get("rarityId"),
                player.get("category"),
                player.get("image")
            ))

            saved += cursor.rowcount

    return saved