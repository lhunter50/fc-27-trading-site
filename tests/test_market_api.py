import requests

url = "https://fc27-market.val.run/history/37576"

response = requests.get(url, timeout=15)
response.raise_for_status()

data = response.json()

print("Response type:", type(data).__name__)
print("Response:", str(data)[:2000])

from datetime import datetime, timezone

timestamps = data["t"]
prices = data["p"]

for timestamp, price in zip(timestamps, prices):
    date = datetime.fromtimestamp(timestamp * 60, tz=timezone.utc)

    print(f"{date} | {price:,} coins")