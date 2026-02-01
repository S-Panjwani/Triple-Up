import time
import numpy as np
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor
import threading
 
import tkinter as tk

# constants
PARTY_EMPTY_POS = (586, 944)
PARTY_EMPTY_COLOR = (0, 0, 0)

CHECK_O_POS = (439, 154)
COLOR_O_NEW = (255, 128, 128)

# board positions
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

# acceptable shades
ACCEPTABLE_COLORS = {
    'X': [(141, 244, 255), (140, 244, 255), (139, 243, 255), (136, 242, 255), (134, 242, 255),
          (134, 242, 255), (137, 243, 255), (135, 242, 255)],
    'O': [(255, 163, 166), (255, 164, 167), (255, 160, 163), (255, 157, 160), (255, 153, 156),
          (255, 162, 165)]
}

def get_color_at_position(position):
    screen = ImageGrab.grab()
    return screen.getpixel(position)

def is_party_full():
    color = get_color_at_position(PARTY_EMPTY_POS)
    return color != PARTY_EMPTY_COLOR

def detect_player_role():
    color = get_color_at_position(CHECK_O_POS)
    return 'O' if color == COLOR_O_NEW else 'X'

def check_square(position, screen_array):
    x, y = position
    radius = 5
    square_value = ' '

    # scan radius
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            current_pos = (x + dx, y + dy)
            if 0 <= current_pos[0] < screen_array.shape[1] and 0 <= current_pos[1] < screen_array.shape[0]:
                color = tuple(screen_array[current_pos[1], current_pos[0]])
                # X
                if color in ACCEPTABLE_COLORS['X']:
                    square_value = 'X'
                    break
                # O
                elif color in ACCEPTABLE_COLORS['O']:
                    square_value = 'O'
                    break

        if square_value != ' ':
            break

    return square_value

def display_board(state, best_move=None):
    # init board
    board = {key: ' ' for key in SQUARE_POSITIONS.keys()}
    # update board
    for key, value in state.items():
        board[key] = value
    # mark best move
    if best_move:
        board[best_move] = 'I'
    # print board
    print("\nCurrent Board:")
    print(f"Top      {board['1']} | {board['2']} | {board['3']}")
    print("         ---------")
    print(f"Middle   {board['4']} | {board['5']} | {board['6']}")
    print("         ---------")
    print(f"Bottom   {board['7']} | {board['8']} | {board['9']}")

def evaluate_winner(board):
    # winning combos
    winning_combinations = [
        ('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'),  # Rows
        ('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9'),  # Columns
        ('1', '5', '9'), ('3', '5', '7')                   # Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]  # Return the winner ('X' or 'O')

    if ' ' not in board.values():
        return 'Draw'

    return None

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

def find_best_move(board, player):
    best_score = float('-inf')
    best_move = None

    for key, value in board.items():
        if value == ' ':
            board[key] = player
            score = minimax(board, 0, False, player)
            board[key] = ' '

            if score > best_score:
                best_score = score
                best_move = key

    return best_move

def board_check(player_role, update_board_func, stop_event):
    prev_states = {key: ' ' for key in SQUARE_POSITIONS.keys()}
    print("Starting checks...")

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

    # Start checking the board in a separate thread; ESC closes window
    player_role = detect_player_role()
    status_label.config(text='STARTING CHECKS..')
    stop_event = threading.Event()
    root.bind('<Escape>', lambda e: stop_event.set())
    board_thread = threading.Thread(target=board_check, args=(player_role, update_board, stop_event))
    board_thread.start()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    main()
