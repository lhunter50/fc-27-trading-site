from app.analysis import scan_market

results = scan_market(min_observations=1)

budget_players = [
    player for player in results
    if player["category"] == "budget"
]

mid_range_players = [
    player for player in results
    if player["category"] == "mid_range"
]

print(f"Total candidates: {len(results)}")
print(f"Budget trading: {len(budget_players)}")
print(f"Mid-range investing: {len(mid_range_players)}")

print("\nBudget trading examples:")
for player in budget_players[:5]:
    print(f"{player['name']}: {player['current_price']:,} coins")

print("\nMid-range examples:")
for player in mid_range_players[:5]:
    print(f"{player['name']}: {player['current_price']:,} coins")


from app.scanner import find_investment_opportunities

opportunities = find_investment_opportunities()

print(f"Investment opportunities: {len(opportunities)}")

for player in opportunities[:10]:
    print(
        f"{player['name']} | "
        f"Buy: {player['current_price']:,} | "
        f"Target: {player['target_price']:,} | "
        f"Profit: {player['potential_profit']:,} | "
        f"ROI: {player['roi']}%"
    )