import random

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Initialize the board
def init_board():
    return [[EMPTY, EMPTY, EMPTY] for _ in range(3)]

# Print the board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# Check if a move is valid
def is_valid_move(board, row, col):
    return board[row][col] == EMPTY

# Make a move
def make_move(board, player, row, col):
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False

# Check for a win
def check_winner(board, player):
    # Check rows, columns, and diagonals
    win_conditions = (
        [board[0], board[1], board[2]],  # Rows
        [[board[0][0], board[1][0], board[2][0]], [board[0][1], board[1][1], board[2][1]], [board[0][2], board[1][2], board[2][2]]],  # Columns
        [board[0][0], board[1][1], board[2][2]],  # Diagonal
        [board[0][2], board[1][1], board[2][0]]   # Anti-diagonal
    )
    for condition in win_conditions:
        if isinstance(condition[0], list):  # For rows and columns
            for line in condition:
                if all(cell == player for cell in line):
                    return True
        else:  # For diagonals
            if all(cell == player for cell in condition):
                return True
    return False

# Check if the board is full
def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Get available moves
def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if is_valid_move(board, r, c)]

# AI: Check for winning move
def aiCanWin(board, player):
    for row in range(3):
        for col in range(3):
            if is_valid_move(board, row, col):
                board[row][col] = player
                if check_winner(board, player):
                    board[row][col] = EMPTY
                    return (row, col)
                board[row][col] = EMPTY
    return None

# AI: Check if blocking is needed
def aiCanBlock(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    return aiCanWin(board, opponent)

# AI: Check if blocking a fork is needed
def aiCanBlockFork(board, player):
    # Check all possible moves to see if they create a fork
    for move in get_available_moves(board):
        row, col = move
        board[row][col] = player
        if is_fork(board, player):
            board[row][col] = EMPTY
            return move
        board[row][col] = EMPTY
    return None

# AI: Check if there is a fork
def is_fork(board, player):
    return any(len(set([board[r][c] for r, c in [(r, c) for r in range(3) for c in range(3) if board[r][c] == player]])) == 2 for row in range(3) for col in range(3) if board[row][col] == EMPTY)

# AI: Check if center is available
def aiCanCenter(board):
    if is_valid_move(board, 1, 1):
        return (1, 1)
    return None

# AI: Check if opposite corner is available
def aiCanFillOppositeCorner(board, player):
    opposite_corners = {
        (0, 0): (2, 2),
        (0, 2): (2, 0),
        (2, 0): (0, 2),
        (2, 2): (0, 0)
    }
    player_corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in player_corners:
        if board[corner[0]][corner[1]] == player:
            opposite = opposite_corners[corner]
            if is_valid_move(board, opposite[0], opposite[1]):
                return opposite
    return None

# AI: Check if any empty corner is available
def aiCanFillEmptyCorner(board):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if is_valid_move(board, corner[0], corner[1]):
            return corner
    return None

# AI: Check if any empty side is available
def aiCanFillEmptySide(board):
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for side in sides:
        if is_valid_move(board, side[0], side[1]):
            return side
    return None

# AI move function
def ai_move(board, player):
    move = aiCanWin(board, player)  # Try to win
    if move:
        return move
    
    move = aiCanBlock(board, player)  # Block opponent
    if move:
        return move

    move = aiCanBlockFork(board, player)  # Block fork
    if move:
        return move

    move = aiCanCenter(board)  # Take center
    if move:
        return move

    move = aiCanFillOppositeCorner(board, player)  # Take opposite corner
    if move:
        return move

    move = aiCanFillEmptyCorner(board)  # Take any empty corner
    if move:
        return move

    move = aiCanFillEmptySide(board)  # Take any empty side
    if move:
        return move

    return random.choice(get_available_moves(board))  # Random move if none of the above

# Main function to run the game
def main():
    board = init_board()
    current_player = PLAYER_X

    while True:
        print_board(board)
        if current_player == PLAYER_X:
            row, col = ai_move(board, PLAYER_X)
            make_move(board, PLAYER_X, row, col)
            if check_winner(board, PLAYER_X):
                print_board(board)
                print("Player X wins!")
                break
        else:
            row, col = ai_move(board, PLAYER_O)
            make_move(board, PLAYER_O, row, col)
            if check_winner(board, PLAYER_O):
                print_board(board)
                print("Player O wins!")
                break

        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O

if __name__ == "__main__":
    main()
