import requests

URL = (
    "https://s3.eu-west-2.amazonaws.com/"
    "game-assets.fut.gg/27/cdn-data/player-prices-ps5.json"
)

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

ids = [int(data["id0"])]

for delta in data["d"]:
    ids.append(ids[-1] + int(delta))

prices = data["p"]

assert len(ids) == len(prices), "Invalid price feed"

print(f"Total priced cards: {len(prices):,}")

for ea_id, price in list(zip(ids, prices))[:5]:
    print(f"Card ID: {ea_id} | Price: {price:,}")

ronaldo = dict(zip(ids, prices)).get(37576)
print("Ronaldo price:", ronaldo)

price_map = dict(zip(ids, prices))

print("\nFeed diagnostics:")
print(f"First ID: {ids[0]}")
print(f"Last ID: {ids[-1]}")
print(f"Unique IDs: {len(set(ids)):,}")
print(f"Total IDs: {len(ids):,}")

print("\nRonaldo diagnostics:")
print(f"Ronaldo exists: {37576 in price_map}")
print(f"Ronaldo price: {price_map.get(37576)}")

print("\nPrice diagnostics:")
print(f"Cards with price > 0: {sum(p > 0 for p in prices):,}")
print(f"Cards with price = 0: {sum(p == 0 for p in prices):,}")

from app.market import get_market_prices

players, updated_at = get_market_prices()

matches = 0
mismatches = []

for player in players:
    ea_id = player["eaId"]
    full_price = price_map.get(ea_id)
    api_price = player.get("price")

    if full_price is None or api_price is None:
        continue

    if full_price == api_price:
        matches += 1
    else:
        mismatches.append({
            "name": player["name"],
            "id": ea_id,
            "full_price": full_price,
            "api_price": api_price
        })

print(f"\nMatching prices: {matches}")
print(f"Mismatching prices: {len(mismatches)}")

for item in mismatches[:10]:
    print(item)


differences = []

for player in players:
    ea_id = player["eaId"]
    full_price = price_map.get(ea_id)
    api_price = player.get("price")

    if not full_price or not api_price:
        continue

    difference = abs(full_price - api_price) / api_price * 100
    differences.append(difference)

print(f"Cards compared: {len(differences)}")
print(f"Within 5%: {sum(d <= 5 for d in differences)}")
print(f"Over 5%: {sum(d > 5 for d in differences)}")
print(f"Over 10%: {sum(d > 10 for d in differences)}")
print(f"Over 20%: {sum(d > 20 for d in differences)}")

budget = 170_000

valid_prices = [p for p in prices if p > 0]

affordable = [p for p in valid_prices if p <= budget]
mid_range = [p for p in valid_prices if 5_000 <= p <= 50_000]
higher_range = [p for p in valid_prices if 50_000 < p <= budget]

print("\nInvestment scanner coverage:")
print(f"Total valid prices: {len(valid_prices):,}")
print(f"Affordable cards: {len(affordable):,}")
print(f"5K–50K cards: {len(mid_range):,}")
print(f"50K–170K cards: {len(higher_range):,}")

from app.scanner import categorize_players

categories = categorize_players(price_map)

print(f"Budget trading candidates: {len(categories['budget']):,}")
print(f"Mid-range candidates: {len(categories['mid_range']):,}")