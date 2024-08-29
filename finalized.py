import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import numpy as np
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor
import threading
import keyboard

# Constants for the known positions and colors
PARTY_EMPTY_POS = (586, 944)
PARTY_EMPTY_COLOR = (0, 0, 0)  # Updated from original color to match the new logic

CHECK_O_POS = (439, 154)
COLOR_O_NEW = (255, 128, 128)  # Light red for O

SQUARE_POSITIONS = {
    '1': [(360, 515), (364, 552)],
    '2': [(483, 513), (485, 552)],
    '3': [(607, 515), (607, 551)],
    '4': [(364, 633), (373, 667)],
    '5': [(483, 633), (482, 668)],
    '6': [(601, 633), (604, 666)],
    '7': [(369, 743), (368, 775)],
    '8': [(483, 743), (519, 745)],
    '9': [(600, 743), (598, 775)]
}

ACCEPTABLE_COLORS = {
    'X': [(141, 244, 255), (140, 244, 255), (139, 243, 255), (136, 242, 255), (134, 242, 255),
          (134, 242, 255), (137, 243, 255), (135, 242, 255)],
    'O': [(255, 163, 166), (255, 164, 167), (255, 160, 163), (255, 157, 160), (255, 153, 156),
          (255, 162, 165)]
}

def get_color_at_position(position):
    screen = ImageGrab.grab()
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
    radius = 5
    square_value = ' '

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            current_pos = (x + dx, y + dy)
            if 0 <= current_pos[0] < screen_array.shape[1] and 0 <= current_pos[1] < screen_array.shape[0]:
                color = tuple(screen_array[current_pos[1], current_pos[0]])
                
                if color in ACCEPTABLE_COLORS['X']:
                    square_value = 'X'
                    break
                elif color in ACCEPTABLE_COLORS['O']:
                    square_value = 'O'
                    break

        if square_value != ' ':
            break

    return square_value

<<<<<<< HEAD
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

=======
>>>>>>> parent of 14ac766 (FINAL VERSION 1)
def evaluate_winner(board):
    winning_combinations = [
        ('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'),
        ('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9'),
        ('1', '5', '9'), ('3', '5', '7')
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]

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

class App:
    def __init__(self, root):
        self.root = root
        root.title("Tic Tac Toe")
        self.update_font_size()
        root.geometry("500x700")
        root.resizable(False, False)

        # Create the status display label
        self.status_label = tk.Label(root, text="Status: N/A", bg="#00aaff", fg="#000000", font=("Arial", self.font_size))
        self.status_label.place(x=125, y=450, width=250, height=50)

        # Create the tic-tac-toe board
        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.place(x=0, y=50)

        # Draw the tic-tac-toe grid
        self.canvas.create_line(167, 0, 167, 400, width=5)
        self.canvas.create_line(333, 0, 333, 400, width=5)
        self.canvas.create_line(0, 133, 500, 133, width=5)
        self.canvas.create_line(0, 267, 500, 267, width=5)

        # Create text labels for each square on the canvas
        self.squares = {
            '1': self.canvas.create_text(83.5, 66.5, text="  ", font=("Arial", self.font_size)),
            '2': self.canvas.create_text(250, 66.5, text="  ", font=("Arial", self.font_size)),
            '3': self.canvas.create_text(416.5, 66.5, text="  ", font=("Arial", self.font_size)),
            '4': self.canvas.create_text(83.5, 200, text="  ", font=("Arial", self.font_size)),
            '5': self.canvas.create_text(250, 200, text="  ", font=("Arial", self.font_size)),
            '6': self.canvas.create_text(416.5, 200, text="  ", font=("Arial", self.font_size)),
            '7': self.canvas.create_text(83.5, 333.5, text="  ", font=("Arial", self.font_size)),
            '8': self.canvas.create_text(250, 333.5, text="  ", font=("Arial", self.font_size)),
            '9': self.canvas.create_text(416.5, 333.5, text="  ", font=("Arial", self.font_size))
        }

        self.current_board = {key: ' ' for key in SQUARE_POSITIONS.keys()}
        self.update_status("PARTY IS EMPTY")

    def update_font_size(self):
        # Calculate the font size based on the size of the canvas and the grid cells
        self.canvas_width = 500
        self.canvas_height = 400
        self.cell_size = self.canvas_width / 3
        self.font_size = int(self.cell_size / 2.5)  # Adjust font size ratio if needed

    def update_status(self, message):
        self.status_label.config(text=message)

    def update_board(self, state, best_move=None):
        for key, value in state.items():
            self.canvas.itemconfig(self.squares[key], text=value if value != ' ' else " ")
        if best_move:
            self.canvas.itemconfig(self.squares[best_move], text="i")

    def board_check(self, player_role):
        prev_states = {key: ' ' for key in SQUARE_POSITIONS.keys()}
        print("Starting checks...")

        stop_event = threading.Event()

        def monitor_keyboard(stop_event):
            print("Press ESC to exit.")
            while not stop_event.is_set():
                if keyboard.is_pressed('esc'):
                    stop_event.set()
                    break

        keyboard_thread = threading.Thread(target=monitor_keyboard, args=(stop_event,))
        keyboard_thread.start()

        while not stop_event.is_set():
            screen = ImageGrab.grab()
            screen_array = np.array(screen)

            current_state = {}
            for key, (x, y) in SQUARE_POSITIONS.items():
                current_state[key] = check_square((x, y), screen_array)
            
            if current_state != prev_states:
                prev_states = current_state
                print("Board state changed")
                self.update_board(current_state)
            
            winner = evaluate_winner(current_state)
            if winner:
                if winner == 'Draw':
                    self.update_status("The game is a draw!")
                else:
                    self.update_status(f"Player {winner} has won!")
                break

            time.sleep(1)

        self.update_status("Exiting...")

def main():
    root = tk.Tk()
    app = App(root)

    root.update()  # Update the UI to ensure the status label is visible immediately

    print("Checking if the party is full...")

    was_party_empty = True

    while True:
        if is_party_full():
            if was_party_empty:
                app.update_status("A player has joined the round. Waiting 15 seconds before checking player role...")
                time.sleep(15)
                was_party_empty = False

            role = detect_player_role()
            if role:
                print(f"You are playing as: {role}")
                app.update_status(f"You are playing as: {role}")
                app.board_check(role)
            break
        else:
            was_party_empty = True
        time.sleep(0.25)

    root.mainloop()

if __name__ == "__main__":
    main()
