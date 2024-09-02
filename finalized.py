import time
import numpy as np
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor
import threading
import keyboard
import tkinter as tk

# Constants for the known positions and colors
PARTY_EMPTY_POS = (586, 944)
PARTY_EMPTY_COLOR = (0, 0, 0)

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
    radius = 10  # Increase radius for better detection
    square_value = ' '  # Default value for empty square

    # Define a color detection threshold
    COLOR_THRESHOLD = 30

    def is_color_close(color1, color2, threshold):
        return all(abs(c1 - c2) <= threshold for c1, c2 in zip(color1, color2))

    # Check a 10-pixel radius around the point
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            current_pos = (x + dx, y + dy)
            if 0 <= current_pos[0] < screen_array.shape[1] and 0 <= current_pos[1] < screen_array.shape[0]:
                color = tuple(screen_array[current_pos[1], current_pos[0]])

                # Check for X
                if any(is_color_close(color, ref_color, COLOR_THRESHOLD) for ref_color in ACCEPTABLE_COLORS['X']):
                    square_value = 'X'
                    break
                # Check for O
                elif any(is_color_close(color, ref_color, COLOR_THRESHOLD) for ref_color in ACCEPTABLE_COLORS['O']):
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
        board[best_move] = 'i'

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

def ai_can_win(board, player):
    # Check for immediate winning move
    for key in board.keys():
        if board[key] == ' ':
            board[key] = player
            if evaluate_winner(board) == player:
                return key
            board[key] = ' '
    return None

def ai_can_block(board, player):
    opponent = 'O' if player == 'X' else 'X'
    return ai_can_win(board, opponent)

def ai_can_block_fork(board, player):
    opponent = 'O' if player == 'X' else 'X'
    forks = []

    for key, value in board.items():
        if value == ' ':
            board[key] = opponent
            if is_fork_possible(board, opponent):
                forks.append(key)
            board[key] = ' '

    if forks:
        return forks[0]  # Block the first found fork
    return None

def is_fork_possible(board, player):
    win_combinations = [
        ('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'),
        ('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9'),
        ('1', '5', '9'), ('3', '5', '7')
    ]

    fork_positions = set()

    for combo in win_combinations:
        line = [board[pos] for pos in combo]
        if line.count(player) == 2 and line.count(' ') == 1:
            fork_positions.add(combo)

    return len(fork_positions) >= 2

def find_best_move(board, player):
    opponent = 'O' if player == 'X' else 'X'  # Define the opponent

    # 1. Check for immediate winning move
    best_move = ai_can_win(board, player)
    if best_move:
        return best_move

    # 2. Block opponent's winning move
    best_move = ai_can_block(board, player)
    if best_move:
        return best_move

    # 3. Block opponent's fork
    best_move = ai_can_block_fork(board, player)
    if best_move:
        return best_move

    # 4. Create a fork
    possible_moves = [key for key, value in board.items() if value == ' ']
    for move in possible_moves:
        board[move] = player
        if is_fork_possible(board, player):
            return move
        board[move] = ' '

    # 5. Take center if available
    if board['5'] == ' ':
        return '5'

    # 6. Play opposite corner
    opposite_corners = [('1', '9'), ('3', '7')]
    for corner1, corner2 in opposite_corners:
        if board[corner1] == opponent and board[corner2] == ' ':
            return corner2
        if board[corner2] == opponent and board[corner1] == ' ':
            return corner1

    # 7. Take any empty corner
    corners = ['1', '3', '7', '9']
    for corner in corners:
        if board[corner] == ' ':
            return corner

    # 8. Take any empty side
    sides = ['2', '4', '6', '8']
    for side in sides:
        if board[side] == ' ':
            return side

    return None

def board_check(player_role, update_board_func):
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

        update_board_func(prev_states, best_move)  # Update the UI board with the best move marked

        # Print the current board status
        display_board(prev_states, best_move)
        
        # Delay before the next check
        time.sleep(1)

    print("Exiting...")

def main():
    global board_labels

    # Initialize the Tkinter UI
    root = tk.Tk()
    root.title("Tic Tac Toe AI")

    # Create status label
    status_label = tk.Label(root, text='PARTY IS EMPTY', font=('Helvetica', 16))
    status_label.pack(pady=10)

    # Create board labels
    board_frame = tk.Frame(root)
    board_frame.pack()

    board_labels = {}
    for i in range(3):
        for j in range(3):
            key = str(i * 3 + j + 1)
            label = tk.Label(board_frame, text=' ', width=5, height=2, borderwidth=2, relief='solid', font=('Helvetica', 24))
            label.grid(row=i, column=j, padx=5, pady=5)
            board_labels[key] = label

    def update_board(state, best_move=None):
        for key, value in state.items():
            board_labels[key].config(text=value)
        if best_move:
            board_labels[best_move].config(text='i', fg='red')

    # Start checking the board in a separate thread
    player_role = detect_player_role()
    print(f"Detected Player Role: {player_role}")  # Show the detected player role
    status_label.config(text='STARTING CHECKS..')
    board_thread = threading.Thread(target=board_check, args=(player_role, update_board))
    board_thread.start()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    main()
