from datetime import datetime, timezone
from app.market import get_market_prices
from app.database import (
    initialize_database,
    initialize_players_table,
    save_prices,
    save_players
)
import time

from app.database import initialize_database, initialize_players_table, save_prices

def collect_prices():
    initialize_database()
    initialize_players_table()

    players, updated_at = get_market_prices()

    save_players(players)

    collected_at = datetime.now(timezone.utc).isoformat()
    saved = save_prices(players, collected_at)

    saved_players = save_players(players)
    saved_prices = save_prices(players, updated_at)

    print(f"Players received: {len(players)}")
    print(f"Player records processed: {saved_players}")
    print(f"New price observations saved: {saved_prices}")
    print(f"Source last updated: {updated_at}")
    print(f"Prices collected at: {collected_at}\n")


if __name__ == "__main__":
    try:
        while True:
            try:
                collect_prices()
            except Exception as error:
                print(f"Collection failed: {error}")

            print("Next check in 15 minutes...\n")
            time.sleep(900)

    except KeyboardInterrupt:
        print("\nCollector stopped.")