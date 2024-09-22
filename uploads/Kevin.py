def serialize_game_state(game_state):
    """Convert game state dictionary to a comma-separated string."""
    cards_str = ','.join(game_state['cards'])  # Convert list of cards to a string
    players_str = ','.join(game_state['players'])  # Convert list of players to a string
    
    # Construct the string
    serialized = (f"Cards: [{cards_str}], "
                  f"Turn: {game_state['turn']}, "
                  f"Last Action: {game_state['last_action']}, "
                  f"Turn Player: {game_state['turn_player']}, "
                  f"Pot: {game_state['pot']}, "
                  f"Winner: {game_state['winner']}, "
                  f"Players: [{players_str}]")
    return serialized
def write_player_data(player_id, action, amt_bet, money):
    """Write player data to a string based on parameters."""
    # Construct the string
    return f"{player_id},{action},{False},{amt_bet},,{money}"
def updateGameState(game_state, id):
    return write_player_data(id, 2, 20, 100)
