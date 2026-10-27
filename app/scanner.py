from app.analysis import scan_market
from app.trading import calculate_profit, calculate_roi
BUDGET = 170_000

PRICE_RANGES = {
    "budget": (1_000, 10_000),
    "mid_range": (10_001, 100_000)
}


def categorize_players(price_map):
    categories = {
        "budget": [],
        "mid_range": []
    }

    for ea_id, price in price_map.items():
        if not isinstance(price, (int, float)) or price <= 0:
            continue

        for category, (minimum, maximum) in PRICE_RANGES.items():
            if minimum <= price <= maximum and price <= BUDGET:
                categories[category].append({
                    "eaId": ea_id,
                    "price": price
                })
                break

    return categories

def find_investment_opportunities(min_observations=2):
    players = scan_market(min_observations=min_observations)
    opportunities = []

    for player in players:
        current_price = player["current_price"]
        average_price = player["average_price"]

        # Need historical observations before evaluating a trade
        if player["observations"] < 2:
            continue

        # Only consider cards below their historical average
        if current_price >= average_price:
            continue

        potential_profit = calculate_profit(
            current_price,
            average_price
        )

        roi = calculate_roi(
            current_price,
            average_price
        )

        if potential_profit <= 0:
            continue

        opportunities.append({
            **player,
            "target_price": average_price,
            "potential_profit": round(potential_profit),
            "roi": round(roi, 2)
        })

    return sorted(
        opportunities,
        key=lambda player: player["roi"],
        reverse=True
    )

def get_scanner_summary(min_observations=2):
    players = scan_market(min_observations=min_observations)

    below_average = 0
    rejected_after_tax = 0
    profitable_opportunities = 0

    for player in players:
        current_price = player["current_price"]
        average_price = player["average_price"]

        if current_price >= average_price:
            continue

        below_average += 1

        potential_profit = calculate_profit(
            current_price,
            average_price
        )

        if potential_profit <= 0:
            rejected_after_tax += 1

        else:
            profitable_opportunities += 1

    return {
        "players_analyzed": len(players),
        "below_average": below_average,
        "rejected_after_tax": rejected_after_tax,
        "profitable_opportunities": profitable_opportunities
    }