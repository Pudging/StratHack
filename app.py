from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, send_from_directory, render_template_string
from werkzeug.utils import secure_filename
import importlib.util
import subprocess
import random
import os

UPLOAD_FOLDER = '/Users/zhaoj/OneDrive/Desktop/FlaskPoker/uploads'
ALLOWED_EXTENSIONS = {'py', 'java', 'cpp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "incredibly secret key"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def call_function(function_name, filename):
    file_path = "/Users/zhaoj/OneDrive/Desktop/FlaskPoker/uploads/" + filename
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("your_script_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Call the specified function
    result = getattr(module, function_name)(game_state, filename[:-3])
    
    return result
def call_daily(function_name, filename):
    file_path = "/Users/zhaoj/OneDrive/Desktop/FlaskPoker/uploads/" + filename
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("your_script_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Call the specified function
    result = getattr(module, function_name)(daily_state, filename[:-3])
    
    return result

@app.route('/')
def home():
    global players
    global daily_players
    global game_state
    global daily_state
    game_state['players'] =[]
    players.clear()
    daily_players.clear()
    daily_state['cards'] = []
    return render_template('index.html')

@app.route('/poker-tutorial')
def pokerTutorial():
    return render_template('pokertutorial.html')
@app.route('/over-under-tutorial')
def overUnderTutorial():
    return render_template('higherorlower.html')
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    filename = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if os.path.exists(file_path):
                os.remove(file_path)

            file.save(file_path)
            return redirect(url_for('upload_file', name=filename))

    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    filename = request.args.get('name')
    file_exists = filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))     
    
    return render_template('upload.html', filename=filename, file_exists=file_exists, uploaded_files=uploaded_files)

@app.route('/delete/<name>', methods=['POST', 'GET'])
def delete_file(name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(name))
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File deleted successfully!')
    else:
        flash('File not found!')
    return redirect(url_for('upload_file'))

bot_files = []
@app.route('/run_files', methods=['POST'])
def run_files():
    global bot_files
    bot_files = []
    
    if 'files[]' in request.form:
        bot_files = request.form.getlist('files[]')
        flash(f'Running the following files: {", ".join(bot_files)}')
    else:
        flash('No files selected to run.')

    return redirect(url_for('upload_file'))


#Script running
def run_script(path):
    try:
        # Adjust the path to your script file
        result = subprocess.run(['python', path], capture_output=True, text=True)
        return jsonify({'output': result.stdout.strip(), 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Code for general Gamestate
game_state = {
    'cards': [],
    'turn': 0,
    'last_action': None,
    'turn_player': 0,
    'pot': 0,
    'winner':0,
    'players':[],
    'recent_actions': [],
    'highest_total_bet':0
}

daily_state = {
    'cards':[],
    'winner':None,
    'winner_points':0
}

daily_players = {
}

def initialize_daily_player(filename):
    player_id = filename[:-3]
    if player_id not in daily_players:
        daily_players[player_id] = {
            'higher':-1,
            'points':0,
            'filename':filename
}
        
@app.route('/api/daily_state')
def get_daily():

    return jsonify(daily_state)

@app.route('/api/daily_players')
def get_daily_players():

    return jsonify(daily_players)


# Code for
players = {}

# Helper function to initialize a player
def initialize_player(filename):
    player_id = filename[:-3]
    if player_id not in players:
        players[player_id] = {
            'action': 0,
            'turn_player': False,
            'amt_bet': 0,
            'cards': [],
            'money': 100,
            'filename':filename,
            'folded': False
}
        
def write_player_data(player_id, action, amt_bet, money):
    """Write player data to a string based on parameters."""
    if player_id not in players:
        return None  # Or handle the case where player does not exist
    
    # Construct the string
    return f"{player_id},{action},{players[player_id]['turn_player']},{amt_bet},,{money}"

def parse_player_data(data_string):
    # """Parse player data from a string."""
    parts = data_string.split(',')
    
    # # Check if parts are enough to unpack values
    if len(parts) < 6:
        print("Error: Invalid data string")
        return  # Handle error for invalid data
    
    player_id = (parts[0])
    
    try:
        action = int(parts[1])  # Convert action to int
    except ValueError:
        print("Error: Action is not a valid integer")
        return  # Handle conversion error

    turn_player = parts[2].strip() == 'True'  # Ensure we strip any whitespace
    try:
        amt_bet = int(parts[3])  # Convert amount bet to int
        money = int(parts[-1])  # Convert money to int
    except ValueError:
        print("Error: Amount bet or money is not a valid integer")
        return  # Handle conversion error

    # Initialize cards as an empty list
    cards = []  # Always set cards to empty

    # Initialize or update the player in the global players dictionary
    players[player_id] = {
        'action': action,
        'turn_player': turn_player,
        'amt_bet': amt_bet,
        'cards': players[player_id]['cards'],  # Set cards to an empty list
        'money': players[player_id]['money'],
        'filename': players[player_id]['filename'],
        'folded': players[player_id]['folded']
    }
@app.route('/api/players')
def get_players():

    return jsonify(players)
#Game Mechanics
from collections import Counter

def card_value(card):
    """Returns the numeric value of a card for comparison."""
    value_str = card[0]
    if value_str == 'A':
        return 14
    elif value_str == 'K':
        return 13
    elif value_str == 'Q':
        return 12
    elif value_str == 'J':
        return 11
    elif value_str == 'T':
        return 10
    else:
        return int(value_str)

def hand_rank(cards):
    """Returns the rank of a poker hand."""
    values = sorted([card_value(card) for card in cards], reverse=True)
    value_counts = Counter(values)
    counts = sorted(value_counts.values(), reverse=True)
    unique_values = sorted(value_counts.keys(), reverse=True)
    
    is_flush = len(set(card[1] for card in cards)) == 1
    is_straight = len(unique_values) == 5 and (unique_values[0] - unique_values[-1] == 4)
    
    if is_straight and is_flush:
        return (8, unique_values[0])  # Straight Flush
    if counts == [4, 1]:
        return (7, unique_values)  # Four of a Kind
    if counts == [3, 2]:
        return (6, unique_values)  # Full House
    if is_flush:
        return (5, unique_values)  # Flush
    if is_straight:
        return (4, unique_values)  # Straight
    if counts == [3, 1, 1]:
        return (3, unique_values)  # Three of a Kind
    if counts == [2, 2, 1]:
        return (2, unique_values)  # Two Pair
    if counts == [2, 1, 1, 1]:
        return (1, unique_values)  # One Pair
    return (0, unique_values)  # High Card

def best_hand(player_cards, community_cards):
    """Returns the best hand rank for a player's cards combined with community cards."""
    all_cards = player_cards + community_cards
    best_rank = (0, [])
    
    # Check all combinations of 5 cards from 7
    from itertools import combinations
    for combo in combinations(all_cards, 5):
        current_rank = hand_rank(combo)
        if current_rank > best_rank:
            best_rank = current_rank
    
    return best_rank

def determine_winner(player_hands, community_cards):
    """Determines the winning player based on the best hand."""
    best_player_id = None
    highest_hand_rank = (0, [])
    
    for player_id, player_cards in player_hands.items():
        hand_rank_value = best_hand(player_cards, community_cards)
        print(f"Player {player_id} has hand rank {hand_rank_value}.")  # Debug line
        
        if hand_rank_value > highest_hand_rank:
            highest_hand_rank = hand_rank_value
            best_player_id = player_id
    
    return best_player_id

def build_player_hands(player_ids):
    """Creates a dictionary with player IDs as keys and their cards as values."""
    player_hands = {}
    for player_id in player_ids:
        if player_id in players:  # Check if the player exists
            player_hands[player_id] = players[player_id].get('cards', [])  # Use .get() to avoid KeyError
        else:
            player_hands[player_id] = []  # Assign empty list if player doesn't exist
    return player_hands




uits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
deck = [f"{value}{suit_index + 1}" for suit_index in range(4) for value in values]
def start_round():
    print(deck)
    # Use the global deck defined above
    random.shuffle(deck)  # Shuffle the deck

    for player_id in players:
        # Deal two cards
        cards_dealt = []
        for _ in range(2):
            if deck:  # Check if there are cards left in the deck
                card = deck.pop(0)  # Remove the card from the deck
                cards_dealt.append(card)
        players[player_id]['cards'] = cards_dealt  # Update the player's cards
    game_state['turn_player'] = 0
    
    
    
def reset_game():
    global deck
    global roundFinished
    roundFinished = False
    
    deck = [f"{value}{suit_index + 1}" for suit_index in range(4) for value in values]
    random.shuffle(deck)
    game_state['cards'] = []
    game_state['turn'] = 0
    for player_id in players:
        players[player_id]['cards'] =[]
        players[player_id]['action'] = 0
        players[player_id]['bet'] = 0 
        players[player_id]['folded'] = False
    game_state['winner'] = []
    game_state['recent_actions'] = []
    game_state['turn_player'] = 0
    game_state['highest_total_bet'] = 0
    
    
@app.route('/realPoker')
def realPoker():
    
    global bot_files
    global players
    global deck
    print(bot_files)
    for x in bot_files:
        game_state['players'].append(x)
    print("Game Files:" + str(game_state['players']))
    for id in game_state['players']:
        initialize_player(id)
    return render_template('PokerRemake.html', game_state= game_state, players=players)
            

roundFinished = False

@app.route('/realPoker/playRound', methods=['GET', 'POST'])
def play_round():
    
    global roundFinished
    if(len(game_state['players'])) == 0:
         game_state['recent_actions'].append("NO DATA! HIT RESET WHEN THERE IS DATA") 
         roundFinished = True
    if(roundFinished): 
        return redirect(url_for('realPoker'))
    start_round()
    global players
    player_ids = list(players.keys())
    while True:
        action_map = {1: 'Check', 2: 'Bet', 3: 'Fold'}
        # Advance the game state
        for player_id in player_ids: 
            print(players[player_id]['money'])
        if game_state['turn_player'] >= len(player_ids):
            if game_state['turn'] == 0:
                game_state['turn_player'] = 0
                game_state['pot'] = sum(players[player_id]['amt_bet'] for player_id in player_ids if player_id in players)
                game_state['turn'] = 1
                game_state['cards'].extend([deck.pop(0) for _ in range(3)])  # Deal 3 cards
                random.shuffle(deck)
            elif game_state['turn'] == 1:
                game_state['turn_player'] = 0
                game_state['pot'] = sum(players[player_id]['amt_bet'] for player_id in player_ids if player_id in players)
                game_state['turn'] = 2
                game_state['cards'].append(deck.pop(0))  # Deal 1 card
            elif game_state['turn'] == 2:
                game_state['turn_player'] = 0
                game_state['pot'] = sum(players[player_id]['amt_bet'] for player_id in player_ids if player_id in players)
                game_state['turn'] = 3
                game_state['cards'].append(deck.pop(0))  # Deal 1 card
            elif game_state['turn'] == 3:
                game_state['turn_player'] = 0
                game_state['pot'] = sum(players[player_id]['amt_bet'] for player_id in player_ids if player_id in players)
                game_state['turn'] = 4
                active_player_ids = [player_id for player_id in player_ids if not players[player_id]['folded']]
                idWinner = determine_winner(build_player_hands(active_player_ids), game_state['cards'])
                players[idWinner]['money'] += game_state['pot']
                game_state['winner'] = idWinner
                print(f"Winner: {idWinner} wins the pot of {game_state['pot']}")
                game_state['pot'] = 0
                
                # Reset bets and money for the next round
                for player_id in player_ids:
                    bet = players[player_id]['amt_bet']
                    players[player_id]['money'] -= bet  # Subtract bet from balance
                    players[player_id]['amt_bet'] = 0  # Reset bet to zero
                
                roundFinished = True
                break
                # Check if game should continue (e.g., check if players have money)
                if all(players[player_id]['money'] <= 0 for player_id in player_ids):
                    print("Game over: All players are out of money.")
                    break
            
        else:
            # Player's turn
            id = player_ids[game_state['turn_player']]
            filename = players[id].get('filename')
            result = call_function("updateGameState", filename)
            
            parse_player_data(result)   
            action = players[id]['action']
            action_str = action_map.get(action, 'Unknown Action')  # Map action to string
            #game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent action
            

            prev_bet = max(players[player_id]['amt_bet'] for player_id in player_ids if player_id != id) if game_state['turn_player'] > 0 else 0

            if action == 1:  # Check
                    if players[id]['amt_bet'] <= prev_bet:
                        
                        action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                        if(players[id]['folded'] != True):
                            game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                        players[id]['folded'] = True
                    elif players[id]['amt_bet'] >=0:
                       
                        action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                        if(players[id]['folded'] != True):
                            game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                        players[id]['folded'] = True
                    # Player's bet remains the same
                    else:
                        action_str = action_map.get(1, 'Unknown Action')  # Map action to string
                        game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                        pass
            elif action == 2:  # Bet
                    if players[id]['amt_bet'] <= prev_bet:
                        print(f"Player {id} folded due to insufficient bet.")
                        action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                        if(players[id]['folded'] != True):
                            game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                        players[id]['folded'] = True
                    else:
                        # Set the bet to the current player's bet (if it was a valid bet)
                    
                        players[id]['amt_bet'] = players[id]['amt_bet']  # This could be the same or a new value depending on your logic
                        action_str = action_map.get(2, 'Unknown Action')  # Map action to string
                        if (game_state['highest_total_bet'] != players[id]['amt_bet']):
                            game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                        game_state['highest_total_bet'] = players[id]['amt_bet']
            elif action == 3:  # Fold
    
                    print(f"Player {id} has folded.")
                    action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                    if(players[id]['folded'] != True):
                            game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                    players[id]['folded'] = True # Log recent actio
            
            # Move to the next player's turn
            game_state['turn_player'] += 1
        if game_state['turn_player'] >= len(player_ids):
            while True:
                # Check if all active players have the same bet or have folded
                active_bets = {players[player_id]['amt_bet'] for player_id in player_ids if not players[player_id]['folded']}
                
                largest_bet = max(active_bets) if active_bets else 0
                game_state['highest_total_bet'] = largest_bet
                if len(active_bets) == 1 or len(active_bets) == 0:
                    break  # Exit the loop if all bets are the same or if all but one player has folded

                # Prompt players for action again
                for player_id in player_ids:
                    if not players[player_id]['folded']:
                        filename = players[player_id].get('filename')
                        if filename:
                            print(f"Player {player_id}'s turn for additional action.")
                            result = call_function("updateGameState", filename)
                            parse_player_data(result)
                            action = players[id]['action']
            
                            if action == 1:  # Check
                                if players[id]['amt_bet'] <= prev_bet:
                                  
                                    action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                                    if(players[id]['folded'] != True):
                                       game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                                    players[id]['folded'] = True
                                elif players[id]['amt_bet'] >=0:
                                   
                                    action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                                    if(players[id]['folded'] != True):
                                        game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                                    players[id]['folded'] = True
                                # Player's bet remains the same
                                else:
                                    action_str = action_map.get(1, 'Unknown Action')  # Map action to string
                                    game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                                    pass
                            elif action == 2:  # Bet
                                if players[id]['amt_bet'] <= prev_bet:
                                    
                                    print(f"Player {id} folded due to insufficient bet.")
                                    action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                                    if(players[id]['folded'] != True):
                                         game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                                    players[id]['folded'] = True  # Log recent actio
                                else:
                                    # Set the bet to the current player's bet (if it was a valid bet)
                                    game_state['highest_total_bet'] = players[id]['amt_bet']
                                    players[id]['amt_bet'] = players[id]['amt_bet']  # This could be the same or a new value depending on your logic
                                    action_str = action_map.get(2, 'Unknown Action')  # Map action to string
                                    game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                            elif action == 3:  # Fold
                                
                                print(f"Player {id} has folded.")
                                action_str = action_map.get(3, 'Unknown Action')  # Map action to string
                                if(players[id]['folded'] != True):
                                     game_state['recent_actions'].append(f"{id} performed action: {action_str}")  # Log recent actio
                                players[id]['folded'] = True
                        
                                        
                            

                # Check if all bets are equal again
                active_bets = {players[player_id]['amt_bet'] for player_id in player_ids if not players[player_id]['folded']}
                if len(active_bets) == 1 or len(active_bets) == 0:
                    break  # Exit the loop if all bets are the same or if all but one player has folded
    return redirect(url_for('realPoker'))



@app.route('/api/gamestate', methods=['GET'])
def get_game_state():
    return jsonify(game_state)

@app.route('/realPoker/reset_round', methods=['POST'])
def reset_round():
    reset_game()
    return redirect(url_for('realPoker'))


@app.route('/daily')
def daily():
    global bot_files
    y =[]
    for x in bot_files:
       y.append(x)
    for id in y:
        initialize_daily_player(id)
    return render_template('daily.html', daily_state=daily_state, daily_players=daily_players)



dailyDeck = [f"{value}{suit_index + 1}" for suit_index in range(4) for value in values]
@app.route('/daily/run')
def daily_run():
    global dailyDeck
    dailyDeck = [f"{value}{suit_index + 1}" for suit_index in range(4) for value in values]
    for id in daily_players:
        daily_players[id]['choices'] = []
    for i in range(0, 5):
        for id in daily_players:
            daily_players[id]['higher'] = -1
        random.shuffle(dailyDeck)
        card = dailyDeck.pop(0)  # Remove the card from the deck
        daily_state['cards'].append(card)  
        for id in daily_players:
            filename = daily_players[id].get('filename')
            result = call_function("updateGameState", filename)
            daily_players[id]['higher'] = result
            daily_players[id]['choices'].append(result)
        card2 = dailyDeck.pop(0)
        daily_state['cards'].append(card2)
        for id in daily_players:
            if (card_value(card2) > card_value(card)):
                if(daily_players[id]['higher'] == 1):
                    daily_players[id]['points'] +=1
            elif (card_value(card2) < card_value(card)):
                if(daily_players[id]['higher'] == 0):
                    daily_players[id]['points'] +=1
    winner = max(daily_players.items(), key=lambda x: x[1]['points'])
    daily_state['winner'] = winner[0]  # Store winner ID
    daily_state['winner_points'] = winner[1]['points']  # Store winner point
          
    return redirect(url_for('daily'))



    
    



