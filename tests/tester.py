import json
from pathlib import Path

data = json.loads(Path("player-prices-ps5.json").read_text())

player_ids = [data["id0"]]

for difference in data["d"]:
    player_ids.append(player_ids[-1] + difference)

prices = data["p"]

if len(player_ids) != len(prices):
    raise ValueError("Player IDs and prices don't match")

players = [
    {"eaId": player_id, "price": price}
    for player_id, price in zip(player_ids, prices)
]

print(f"Total priced cards: {len(players):,}")
print("First five:", players[:5])

ronaldo = next(
    (p for p in players if p["eaId"] == 37576),
    None
)

print("Ronaldo:", ronaldo)