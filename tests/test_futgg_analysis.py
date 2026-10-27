from app.futgg_analysis import (
    scan_futgg_market,
    find_futgg_opportunities,
)


def main():
    players = scan_futgg_market(min_observations=1)
    eligible = scan_futgg_market(min_observations=2)
    opportunities = find_futgg_opportunities(min_observations=3)

    print(f"Players analyzed: {len(players):,}")
    print(f"Players with 2+ observations: {len(eligible):,}")
    print(f"Profitable opportunities: {len(opportunities):,}")
    print(len(scan_futgg_market(min_observations=3)))

    print("\nSample players:")

    for player in players[:5]:
        print(
            f"{player['name']} "
            f"| Current: {player['current_price']:,} "
            f"| Average: {player['average_price']:,.0f} "
            f"| Observations: {player['observations']}"
        )


if __name__ == "__main__":
    main()