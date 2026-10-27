
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