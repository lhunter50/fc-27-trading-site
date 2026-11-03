
from app.futgg_analysis import get_recent_price_history



PLAYER_ID = 260456

history = get_recent_price_history(
    player_id=PLAYER_ID,
    days=7,
)

print(f"Observations: {len(history)}")

for observation in history[-10:]:
    print(
        observation["recorded_at"],
        observation["price"],
    )

from app.futgg_analysis import calculate_time_weighted_median

median_price = calculate_time_weighted_median(history)

print(f"\nTime-weighted median: {median_price}")
print(f"Latest recorded price: {history[-1]['price']}")



from datetime import datetime

first_observation = datetime.fromisoformat(
    history[0]["recorded_at"]
)

last_observation = datetime.fromisoformat(
    history[-1]["recorded_at"]
)

duration_hours = (
    last_observation - first_observation
).total_seconds() / 3600

print(f"History duration: {duration_hours:.1f} hours")
print(f"Observations: {len(history)}")

from app.futgg_analysis import evaluate_history_quality

quality = evaluate_history_quality(history)

print(f"History status: {quality['status']}")
print(f"Reason: {quality['reason']}")


from app.futgg_analysis import calculate_price_statistics

stats = calculate_price_statistics(history)

print("\nPrice statistics:")
for key, value in stats.items():
    print(f"{key}: {value}")



from app.futgg_analysis import evaluate_investment

investment = evaluate_investment(history)

print("\nInvestment evaluation:")
for key, value in investment.items():
    print(f"{key}: {value}")



from app.futgg_analysis import calculate_price_trend

trend = calculate_price_trend(history)

print("\nPrice trend:")
for key, value in trend.items():
    print(f"{key}: {value}")
