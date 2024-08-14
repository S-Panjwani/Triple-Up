import time
from PIL import ImageGrab

# Constants for the known positions and colors
PARTY_EMPTY_POS = (586, 944)
PARTY_EMPTY_COLOR = (0, 0, 0)  # Updated from original color to match the new logic

# New position and color for determining if the player is O
CHECK_O_POS = (439, 154)
COLOR_O_NEW = (255, 128, 128)  # Light red for O

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
    if color == COLOR_O_NEW:
        return 'O'
    else:
        return 'X'

def main():
    print("Checking if the party is full...")

    was_party_empty = True
    
    while True:
        if is_party_full():
            if was_party_empty:
                print("A player has joined the round. Waiting 10 seconds before checking player role...")
                time.sleep(10)  # Delay for 10 seconds before detecting the role
                was_party_empty = False  # Mark party as not empty
            
            # Determine the player's role (X or O)
            role = detect_player_role()
            if role:
                print(f"You are playing as: {role}")
                
                # Run the additional script after determining the role
                import numpy as np
                from concurrent.futures import ThreadPoolExecutor
                import threading
                import keyboard  # For detecting key presses

                # Define positions for the Tic Tac Toe board
                SQUARE_POSITIONS = {
    'TOP-LEFT X': (360, 515),
    'TOP-LEFT O': (364, 552),
    'TOP-MIDDLE X': (483, 513),
    'TOP-MIDDLE O': (485, 552),
    'TOP-RIGHT X': (607, 515),
    'TOP-RIGHT O': (607, 551),
    'TOP-RIGHT X': (608, 514),
    'MIDDLE-LEFT X': (364, 633),
    'MIDDLE-LEFT O': (373, 667),
    'MIDDLE-MIDDLE X': (483, 633),
    'MIDDLE-MIDDLE O': (482, 668),
    'MIDDLE-RIGHT X': (601, 633),
    'MIDDLE-RIGHT O': (604, 666),
    'BOTTOM-LEFT X': (369, 743),
    'BOTTOM-LEFT O': (368, 775),
    'BOTTOM-MIDDLE X': (483, 743),
    'BOTTOM-MIDDLE O': (519, 745),
    'BOTTOM-RIGHT X': (600, 743),
    'BOTTOM-RIGHT O': (598, 775)
                }

                # Define acceptable shades of colors
                ACCEPTABLE_COLORS = {
                    'X': [(141, 244, 255), (140, 244, 255), (139, 243, 255), (136, 242, 255), (134, 242, 255),  # Updated X colors
                          (134, 242, 255), (137, 243, 255), (135, 242, 255)],
                    'O': [(255, 163, 166), (255, 164, 167), (255, 160, 163), (255, 157, 160), (255, 153, 156),  # Red for O
                          (255, 162, 165)]  # Added new O color
                }

                def get_color_at_position(position, screen_array):
                    x, y = position
                    return tuple(screen_array[y, x])

                def check_square(label, pos, prev_states, screen_array):
                    x, y = pos
                    radius = 5  # Radius around the point to check
                    square_value = ' '  # Default value for empty square

                    # Check a 5-pixel radius around the point
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            current_pos = (x + dx, y + dy)
                            if 0 <= current_pos[0] < screen_array.shape[1] and 0 <= current_pos[1] < screen_array.shape[0]:
                                color = get_color_at_position(current_pos, screen_array)
                                hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
                                
                                # Debugging output
                                print(f"Checking {label} at position {current_pos}: RGB: {color}, Hex: {hex_color}")

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

                def display_board(state):
                    # Define position mappings to numbers
                    position_map = {
                        'TOP-LEFT X': '1', 'TOP-LEFT O': '1',
                        'TOP-MIDDLE X': '2', 'TOP-MIDDLE O': '2',
                        'TOP-RIGHT X': '3', 'TOP-RIGHT O': '3',
                        'MIDDLE-LEFT X': '4', 'MIDDLE-LEFT O': '4',
                        'MIDDLE-MIDDLE X': '5', 'MIDDLE-MIDDLE O': '5',
                        'MIDDLE-RIGHT X': '6', 'MIDDLE-RIGHT O': '6',
                        'BOTTOM-LEFT X': '7', 'BOTTOM-LEFT O': '7',
                        'BOTTOM-MIDDLE X': '8', 'BOTTOM-MIDDLE O': '8',
                        'BOTTOM-RIGHT X': '9', 'BOTTOM-RIGHT O': '9'
                    }

                    # Initialize the board with empty spaces
                    board = {
                        '1': ' ', '2': ' ', '3': ' ',
                        '4': ' ', '5': ' ', '6': ' ',
                        '7': ' ', '8': ' ', '9': ' '
                    }

                    # Update the board with current states
                    for label, value in state.items():
                        if value in ['X', 'O']:
                            board[position_map.get(label, '')] = value

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

                def board_check():
                    prev_states = {label: ' ' for label in SQUARE_POSITIONS.keys()}
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
                                label: executor.submit(check_square, label, pos, prev_states, screen_array)
                                for label, pos in SQUARE_POSITIONS.items()
                            }

                            for label, future in results.items():
                                prev_states[label] = future.result()  # Update the state of each square

                        display_board(prev_states)  # Display the board in the desired format

                        # Delay for a longer interval before the next check
                        time.sleep(1)  # Adjusted delay to 1 second

                    print("Exiting...")

                # Run the board check script
                board_check()

            # Exit the loop once the role has been determined and the board check is running
            break

        else:
            was_party_empty = True  # Reset the empty status if the party is not full

        # Delay before the next check
        time.sleep(1)

    print("Exiting main script...")

if __name__ == "__main__":
    main()
