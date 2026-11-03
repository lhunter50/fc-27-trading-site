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



def get_recent_price_history(player_id: int, days: int = 7):
    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).isoformat()

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT price, recorded_at
            FROM futgg_price_history
            WHERE player_id = ?
              AND recorded_at >= ?
            ORDER BY recorded_at ASC, id ASC
            """,
            (player_id, cutoff),
        ).fetchall()

    return [dict(row) for row in rows]




def calculate_time_weighted_median(history, end_time=None):
    if not history:
        return None

    end_time = end_time or datetime.now(timezone.utc)
    weighted_prices = []

    for index, observation in enumerate(history):
        start = datetime.fromisoformat(observation["recorded_at"])

        if index + 1 < len(history):
            end = datetime.fromisoformat(
                history[index + 1]["recorded_at"]
            )
        else:
            end = end_time

        duration = max((end - start).total_seconds(), 0)
        weighted_prices.append((observation["price"], duration))

    weighted_prices.sort(key=lambda item: item[0])
    total_duration = sum(duration for _, duration in weighted_prices)

    if total_duration <= 0:
        return None

    halfway = total_duration / 2
    accumulated = 0

    for price, duration in weighted_prices:
        accumulated += duration
        if accumulated >= halfway:
            return price

    return weighted_prices[-1][0]




def evaluate_history_quality(history):
    if len(history) < 10:
        return {
            "status": "insufficient_data",
            "reason": "Fewer than 10 observations",
        }

    first = datetime.fromisoformat(
        history[0]["recorded_at"]
    )

    last = datetime.fromisoformat(
        history[-1]["recorded_at"]
    )

    duration_hours = (
        last - first
    ).total_seconds() / 3600

    if duration_hours < 72:
        return {
            "status": "insufficient_data",
            "reason": "Less than 72 hours of history",
        }

    return {
        "status": "eligible",
        "reason": "Minimum history requirements met",
    }


def calculate_price_statistics(history):
    if not history:
        return None

    prices = [row["price"] for row in history]

    weighted_median = calculate_time_weighted_median(history)

    if weighted_median is None:
        return None

    latest_price = history[-1]["price"]

    return {
        "current_price": latest_price,
        "median_price": weighted_median,
        "discount_percent": round(
            (weighted_median - latest_price) / weighted_median * 100, 2
        ),
        "observations": len(history),
        "history_quality": evaluate_history_quality(history)
    } 



def evaluate_investment(history, min_roi=10.0):
    stats = calculate_price_statistics(history)

    if stats is None:
        return None

    buy_price = stats["current_price"]
    sell_target = stats["median_price"]

    profit = calculate_profit(buy_price, sell_target)
    roi = calculate_roi(buy_price, sell_target)


    trend = calculate_price_trend(history)

    if stats["history_quality"]["status"] != "eligible":
        signal = "INSUFFICIENT_DATA"
    elif trend and trend["direction"] == "FALLING":
        signal = "AVOID"
    elif profit <= 0 or roi < min_roi:
        signal = "AVOID"
    else:
        signal = "WATCH"


    return {
        **stats,
        "buy_price": buy_price,
        "sell_target": sell_target,
        "potential_profit": round(profit),
        "roi": round(roi, 2),
        "trend": trend,
        "signal": signal,
    }


def calculate_price_trend(history):
    if len(history) < 10:
        return None

    midpoint = len(history) // 2

    older_history = history[:midpoint]
    recent_history = history[midpoint:]

    older_end = datetime.fromisoformat(
        recent_history[0]["recorded_at"]
    )
    recent_end = datetime.fromisoformat(
        recent_history[-1]["recorded_at"]
    )

    older_median = calculate_time_weighted_median(
        older_history, end_time=older_end
    )
    recent_median = calculate_time_weighted_median(
        recent_history, end_time=recent_end
    )

    if older_median is None or older_median <= 0:
        return None

    change_percent = ((recent_median - older_median) / older_median ) * 100

    if change_percent <= -15:
        direction = "FALLING"
    elif change_percent >= 15:
        direction = "RISING"
    else: 
        direction = "STABLE"

    return {
        "direction": direction,
        "change_percent": round(change_percent, 2),
        "older_median": older_median,
        "recent_median": recent_median,
    }