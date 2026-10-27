import requests

URL = "https://www.fut.gg/api/fut/players/v2/27/"


def main():
    response = requests.get(
        URL,
        params={"page": 1},
        timeout=30,
    )

    print(f"Status: {response.status_code}")
    print(f"Content type: {response.headers.get('Content-Type')}")

    if response.status_code != 200:
        print(response.text[:500])
        return

    data = response.json()

    players = data.get("data", [])

    print(f"Players on page: {len(players)}")
    print(f"Total reported: {data.get('total')}")
    print(f"Next page: {data.get('next')}")

    if players:
        player = players[0]

        print("\nSample metadata:")
        print("EA ID:", player.get("eaId"))
        print("Name:", player.get("commonName"))
        print("Rating:", player.get("overall"))
        print("Rarity:", player.get("rarityName"))

    if isinstance(data, dict):
        print("Top-level keys:", list(data.keys()))

        for key, value in data.items():
            print(f"\n{key}:")
            print(str(value)[:1000])
    else:
        print("Response type:", type(data).__name__)
        print(str(data)[:1000])


if __name__ == "__main__":
    main()