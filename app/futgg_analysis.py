import sqlite3

from datetime import datetime, timedelta, timezone
from app.database import DATABASE
from app.trading import calculate_profit, calculate_roi


def scan_futgg_market(min_observations=2, max_age_minutes=60):
    cutoff = (
        datetime.now(timezone.utc)
        - timedelta(minutes=max_age_minutes)
    ).isoformat()
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT
                p.ea_id AS player_id,
                p.name,
                p.rating,
                p.category,
                COUNT(h.id) AS observations,
                AVG(h.price) AS average_price,
                (
                    SELECT h2.price
                    FROM futgg_price_history h2
                    WHERE h2.player_id = p.ea_id
                    ORDER BY h2.recorded_at DESC, h2.id DESC
                    LIMIT 1
                ) AS current_price
            FROM futgg_players p
            JOIN futgg_price_history h
                ON h.player_id = p.ea_id
            WHERE p.last_seen_at >= ?
            GROUP BY p.ea_id
            HAVING COUNT(h.id) >= ?
        """, (cutoff, min_observations)).fetchall()

    return [dict(row) for row in rows]


def find_futgg_opportunities(min_observations=3):
    players = scan_futgg_market(min_observations)
    opportunities = []

    for player in players:
        current_price = player["current_price"]
        average_price = player["average_price"]

        if current_price >= average_price:
            continue

        profit = calculate_profit(current_price, average_price)

        if profit <= 0:
            continue

        roi = calculate_roi(current_price, average_price)

        opportunities.append({
            **player,
            "target_price": round(average_price),
            "potential_profit": round(profit),
            "roi": round(roi, 2),
        })

    return sorted(
        opportunities,
        key=lambda player: player["roi"],
        reverse=True,
    )