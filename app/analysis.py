import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent.parent / "data" / "market.db"


def get_price_history(player_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("""
            SELECT price, recorded_at
            FROM price_history
            WHERE player_id = ?
            ORDER BY recorded_at ASC
        """, (player_id,))

        return cursor.fetchall()

def analyze_player(player_id):
    history = get_price_history(player_id)

    if not history:
        return None

    prices = [row[0] for row in history]

    current_price = prices[-1]
    average_price = sum(prices) / len(prices)

    price_change = (
        (current_price - prices[0]) / prices[0] * 100
        if len(prices) >= 2 and prices[0] > 0
        else None
    )

    difference_from_average = (
        (current_price - average_price) / average_price * 100
        if average_price > 0 and len(prices) >= 2
        else None
    )

    return {
        "player_id": player_id,
        "current_price": current_price,
        "average_price": round(average_price),
        "price_change": round(price_change, 2) if price_change is not None else None,
        "difference_from_average": (
            round(difference_from_average, 2)
            if difference_from_average is not None
            else None
        ),
        "observations": len(prices)
    }

def scan_market(min_observations=2):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("""
            SELECT ea_id, name
            FROM players
        """)

        players = cursor.fetchall()

    results = []

    for player_id, name in players:
        analysis = analyze_player(player_id)

        if analysis is None:
            continue

        if analysis["observations"] < min_observations:
            continue

        price = analysis["current_price"]

        if price is None or price <= 0:
            continue

        if 1_000 <= price <= 10_000:
            category = "budget"
        elif 10_000 < price <= 100_000:
            category = "mid_range"
        else:
            continue

        analysis["name"] = name
        analysis["category"] = category

        results.append(analysis)

    return results