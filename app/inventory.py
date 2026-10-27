from app.trading import calculate_profit, should_sell


def add_to_inventory(inventory, player):
    inventory_entry = {
        "name": player['name'],
        "buy_price": player['buy_price'],
        "market_value": player['market_value'],
        "expected_profit": calculate_profit(player['buy_price'], player['market_value']),
        "status": "owned",
    }
    inventory.append(inventory_entry)
    return inventory

def sell_player(inventory, player_name, sell_price, balance):
    tax = int(sell_price * 0.05)
    for player in inventory:
        if player['name'] == player_name and player['status'] == "owned":
            profit = calculate_profit(player['buy_price'], sell_price)
            player['status'] = "sold"
            balance += sell_price - tax
            return balance, profit
    raise ValueError(f"Player {player_name} not found in inventory or already sold.")

def evaluate_inventory(inventory, current_prices, min_profit):
    evaluation = []
    for player in inventory:
        current_price = current_prices.get(player['name'])
        if current_price is not None:
            sell_decision = should_sell(player, current_price, min_profit)
            evaluation.append({
                "name": player['name'],
                "buy_price": player['buy_price'],
                "current_price": current_price,
                "expected_profit": calculate_profit(player['buy_price'], current_price),
                "should_sell": sell_decision
            })
    return evaluation