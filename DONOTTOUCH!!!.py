import time
import numpy as np
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor
import threading
import keyboard

# Constants for the known positions and colors
PARTY_EMPTY_POS = (586, 944)
PARTY_EMPTY_COLOR = (0, 0, 0)  # Updated from original color to match the new logic

# New position and color for determining if the player is O
CHECK_O_POS = (439, 154)
COLOR_O_NEW = (255, 128, 128)  # Light red for O

# Define positions for the Tic Tac Toe board
SQUARE_POSITIONS = {
    '1': [(360, 515), (364, 552)],  # TOP-LEFT X, O
    '2': [(483, 513), (485, 552)],  # TOP-MIDDLE X, O
    '3': [(607, 515), (607, 551)],  # TOP-RIGHT X, O
    '4': [(364, 633), (373, 667)],  # MIDDLE-LEFT X, O
    '5': [(483, 633), (482, 668)],  # MIDDLE-MIDDLE X, O
    '6': [(601, 633), (604, 666)],  # MIDDLE-RIGHT X, O
    '7': [(369, 743), (368, 775)],  # BOTTOM-LEFT X, O
    '8': [(483, 743), (519, 745)],  # BOTTOM-MIDDLE X, O
    '9': [(600, 743), (598, 775)]   # BOTTOM-RIGHT X, O
}

# Define acceptable shades of colors
ACCEPTABLE_COLORS = {
    'X': [(141, 244, 255), (140, 244, 255), (139, 243, 255), (136, 242, 255), (134, 242, 255),
          (134, 242, 255), (137, 243, 255), (135, 242, 255)],
    'O': [(255, 163, 166), (255, 164, 167), (255, 160, 163), (255, 157, 160), (255, 153, 156),
          (255, 162, 165)]
}

def get_color_at_position(position):
    # Capture the screen
    screen = ImageGrab.grab()
    # Get the color at the specified position
    color = screen.getpixel(position)
    return color

def is_party_full():
    color = get_color_at_position(PARTY_EMPTY_POS)
    return color != PARTY_EMPTY_COLOR

def detect_player_role():
    color = get_color_at_position(CHECK_O_POS)
    return 'O' if color == COLOR_O_NEW else 'X'

def check_square(position, screen_array):
    x, y = position
    radius = 5  # Radius around the point to check
    square_value = ' '  # Default value for empty square

    # Check a 5-pixel radius around the point
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            current_pos = (x + dx, y + dy)
            if 0 <= current_pos[0] < screen_array.shape[1] and 0 <= current_pos[1] < screen_array.shape[0]:
                color = tuple(screen_array[current_pos[1], current_pos[0]])
                
                # Check for X
                if color in ACCEPTABLE_COLORS['X']:
                    square_value = 'X'
                    break
                # Check for O
                elif color in ACCEPTABLE_COLORS['O']:
                    square_value = 'O'
                    break

        if square_value != ' ':
            break

    return square_value

def display_board(state, best_move=None):
    # Initialize the board with empty spaces
    board = {key: ' ' for key in SQUARE_POSITIONS.keys()}

    # Update the board with current states
    for key, value in state.items():
        board[key] = value

    # Mark the best move
    if best_move:
        board[best_move] = 'I'

    # Display the board in the desired format
    print("\nCurrent Board:")
    print(f"Top      {board['1']} | {board['2']} | {board['3']}")
    print("         ---------")
    print(f"Middle   {board['4']} | {board['5']} | {board['6']}")
    print("         ---------")
    print(f"Bottom   {board['7']} | {board['8']} | {board['9']}")

def monitor_keyboard(stop_event):
    print("Press ESC to exit.")
    keyboard.wait('esc')  # Wait until the ESC key is pressed
    stop_event.set()  # Signal to stop the main loop

def evaluate_winner(board):
    # Define winning combinations
    winning_combinations = [
        ('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'),  # Rows
        ('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9'),  # Columns
        ('1', '5', '9'), ('3', '5', '7')                   # Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]  # Return the winner ('X' or 'O')

    if ' ' not in board.values():
        return 'Draw'  # Return 'Draw' if there are no empty spaces left

    return None  # Return None if there is no winner yet

def minimax(board, depth, is_maximizing, player):
    opponent = 'O' if player == 'X' else 'X'
    winner = evaluate_winner(board)
    if winner == player:
        return 10 - depth
    elif winner == opponent:
        return depth - 10
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for key, value in board.items():
            if value == ' ':
                board[key] = player
                score = minimax(board, depth + 1, False, player)
                board[key] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for key, value in board.items():
            if value == ' ':
                board[key] = opponent
                score = minimax(board, depth + 1, True, player)
                board[key] = ' '
                best_score = min(score, best_score)
        return best_score

def is_fork(board, player):
    opponent = 'O' if player == 'X' else 'X'
    forks = []
    
    for key, value in board.items():
        if value == ' ':
            board[key] = player
            win_paths = [k for k, v in board.items() if v == ' ' and minimax(board, 0, False, player) > 0]
            if len(win_paths) > 1:
                forks.append(key)
            board[key] = ' '

    return forks

def find_best_move(board, player):
    best_score = float('-inf')
    best_move = None

    # Check for potential forks to create
    potential_forks = is_fork(board, player)
    if potential_forks:
        return potential_forks[0]  # Return the first fork opportunity

    for key, value in board.items():
        if value == ' ':
            board[key] = player
            score = minimax(board, 0, False, player)
            board[key] = ' '

            if score > best_score:
                best_score = score
                best_move = key

    return best_move

def board_check(player_role):
    prev_states = {key: ' ' for key in SQUARE_POSITIONS.keys()}
    print("Starting checks...")

    stop_event = threading.Event()

    # Start a separate thread to monitor keyboard input
    keyboard_thread = threading.Thread(target=monitor_keyboard, args=(stop_event,))
    keyboard_thread.start()

    while not stop_event.is_set():
        screen = ImageGrab.grab()
        screen_array = np.array(screen)

        with ThreadPoolExecutor() as executor:
            results = {
                (key, idx): executor.submit(check_square, pos, screen_array)
                for key, pos_list in SQUARE_POSITIONS.items()
                for idx, pos in enumerate(pos_list)
            }

            for key in SQUARE_POSITIONS.keys():
                square_values = [results[(key, idx)].result() for idx, _ in enumerate(SQUARE_POSITIONS[key])]
                prev_states[key] = 'X' if 'X' in square_values else ('O' if 'O' in square_values else ' ')

        best_move = find_best_move(prev_states, player_role)

        display_board(prev_states, best_move)  # Display the board with the best move marked

        # Delay before the next check
        time.sleep(1)

    print("Exiting...")

def main():
    print("Checking if the party is full...")

    was_party_empty = True

    while True:
        if is_party_full():
            if was_party_empty:
                print("A player has joined the round. Waiting 10 seconds before checking player role...")
                time.sleep(15)  # Delay for 10 seconds before detecting the role
                was_party_empty = False  # Mark party as not empty

            # Determine the player's role (X or O)
            role = detect_player_role()
            if role:
                print(f"You are playing as: {role}")

                # Run the board check after determining the role
                board_check(role)

            # Exit the loop once the role has been determined and the board check is running
            break

        else:
            was_party_empty = True  # Reset the empty status if the party is not full

        # Delay before rechecking the party status
        time.sleep(0.25)

if __name__ == "__main__":
    main()
<<<<<<< HEAD:DONOTTOUCH!!!.py
=======
 
>>>>>>> parent of 14ac766 (FINAL VERSION 1):WORKING NO TOUCHY/DONOTTOUCH!!!.py
