def calculate_profit(buy_price, sell_price):
    """
    Calculate the profit from a trade given the buy and sell prices.

    Parameters:
    buy_price (float): The price at which the asset was bought.
    sell_price (float): The price at which the asset was sold.

    Returns:
    float: The profit made from the trade.
    """
    tax = sell_price * 0.05
    profit = sell_price - buy_price - tax
    return profit

def should_buy(buy_price, market_value, min_profit, balance):
    """
    Determine whether to buy an player based on the buy price, market value, minimum profit, and available balance.

    Parameters:
    buy_price (float): The price at which the asset is being considered for purchase.
    market_value (float): The current market value of the asset.
    min_profit (float): The minimum profit required to justify the purchase.
    balance (float): The available balance for making the purchase.

    Returns:
    bool: True if the asset should be bought, False otherwise.
    """
    potential_profit = calculate_profit(buy_price, market_value)

    print(f"Potential profit: ${potential_profit:.2f}, Minimum required profit: ${min_profit:.2f}, Available balance: ${balance:.2f}, Buy price: ${buy_price:.2f}")

    if potential_profit >= min_profit and balance >= buy_price:
        return True
    return False

def find_profitable_players(players, min_profit, balance):
    """
    Find players that can be bought for a profit.

    Parameters:
    players (list): A list of dictionaries containing player information.
    min_profit (float): The minimum profit required to justify the purchase.
    balance (float): The available balance for making purchases.

    Returns:
    list: A list of players that can be bought for a profit.
    """
    profitable_players = []
    for player in players:
        buy_price = player['buy_price']
        market_value = player['market_value']
        if should_buy(buy_price, market_value, min_profit, balance):
            profitable_players.append(player)
    return profitable_players

def rank_players(players, sort_by='profit'):
    """
    Rank players based on their potential profit.

    Parameters:
    players (list): A list of dictionaries containing player information.
    sort_by (str): The metric to sort by ('profit' or 'roi').

    Returns:
    list: A list of players sorted by the specified metric in descending order.
    """
    if sort_by == 'profit':
        ranked_players = sorted(players, key=lambda x: calculate_profit(x['buy_price'], x['market_value']), reverse=True)
    elif sort_by == 'roi':
        ranked_players = sorted(players, key=lambda x: calculate_roi(x['buy_price'], x['market_value']), reverse=True)
    else:
        raise ValueError("Invalid sort_by value. Please choose 'profit' or 'roi'.")
    return ranked_players

def calculate_roi(buy_price, sell_price):
    """
    Calculate the Return on Investment (ROI) for a trade.

    Parameters:
    buy_price (float): The price at which the asset was bought.
    sell_price (float): The price at which the asset was sold.

    Returns:
    float: The ROI expressed as a percentage.
    """
    profit = calculate_profit(buy_price, sell_price)
    roi = (profit / buy_price) * 100 if buy_price != 0 else 0
    return roi

def simulate_purchases(players, balance, min_profit):
    """
    Simulate purchases of players based on available balance and minimum profit.

    Parameters:
    players (list): A list of dictionaries containing player information.
    balance (float): The available balance for making purchases.
    min_profit (float): The minimum profit required to justify the purchase.

    Returns:
    list: A list of players that were successfully purchased.
    """
    ranked_players = rank_players(players, sort_by='roi')

    purchased_players = []

    for player in ranked_players:
        buy_price = player['buy_price']
        market_value = player['market_value']
        if should_buy(buy_price, market_value, min_profit, balance):
            purchased_players.append(player)
            balance -= buy_price  # Deduct the buy price from the available balance
            print(f"Purchased {player['name']} for {buy_price:} coins. Remaining balance: {balance:} coins")
        else:
            print(f"Did not purchase {player['name']}.")
    return purchased_players, balance

def should_sell(player, current_market_price, min_profit):
    """
    Determine whether to sell a player based on the current market price and minimum profit.

    Parameters:
    player (dict): A dictionary containing player information.
    current_market_price (float): The current market price of the player.
    min_profit (float): The minimum profit required to justify the sale.

    Returns:
    bool: True if the player should be sold, False otherwise.
    """
    if player['status'] != "owned":
        print(f"{player['name']} is not owned and cannot be sold.")
        return False
    buy_price = player['buy_price']
    potential_profit = calculate_profit(buy_price, current_market_price)

    print(f"Potential profit from selling {player['name']}: {potential_profit:} coins, Minimum required profit: {min_profit:} coins")


    return potential_profit >=min_profit and player['status'] == "owned"

def simulate_market_change(players, volatility=0.1):
    """
    Simulate market price changes for players based on a given volatility.

    Parameters:
    players (list): A list of dictionaries containing player information.
    volatility (float): The maximum percentage change in market value.

    Returns:
    dict: A dictionary mapping player names to their updated market values.
    """
    import random

    updated_prices = {}

    for player in players:
        change_percentage = random.uniform(-volatility, volatility)
        new_market_value = player['market_value'] * (1 + change_percentage)
        updated_prices[player['name']] = round(new_market_value)
        print(f"Updated market value for {player['name']}: {updated_prices[player['name']]} coins")
    return updated_prices