import requests

URL = "https://www.fut.gg/api/fut/players/v2/27/"

PLAYER_ID = 20801

response = requests.get(
    URL,
    params={"eaId": PLAYER_ID},
    timeout=30,
)

print("Status:", response.status_code)

response.raise_for_status()

data = response.json()

print("Total:", data.get("total"))
print("Results:", len(data.get("data", [])))

for player in data.get("data", [])[:5]:
    print(
        player.get("eaId"),
        player.get("commonName"),
        player.get("overall"),
    )