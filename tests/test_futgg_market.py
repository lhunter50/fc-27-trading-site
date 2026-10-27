from app.futgg_market import fetch_futgg_market


def main():
    players = fetch_futgg_market()

    budget = sum(
        1 for player in players
        if player["category"] == "budget"
    )

    mid_range = sum(
        1 for player in players
        if player["category"] == "mid_range"
    )

    print(f"Total players: {len(players):,}")
    print(f"Budget players: {budget:,}")
    print(f"Mid-range players: {mid_range:,}")

    print("\nSample records:")

    for player in players[:5]:
        print(player)


if __name__ == "__main__":
    main()