import time
from PIL import ImageGrab

# Constants for the known positions and colors
PARTY_EMPTY_POS = (586, 944)
PARTY_EMPTY_COLOR = (0, 0, 0)  # Updated from original color to match the new logic

NEW_ROLE_POS = (520, 153)  # Updated position for role detection
COLOR_X = (255, 128, 128)
COLOR_O = (99, 114, 166)

# Define positions and expected colors for the Tic Tac Toe board
SQUARE_POSITIONS = {
    'TOP-LEFT Center': (360, 515),
    'TOP-LEFT O Spot': (364, 552),
    'TOP-MIDDLE Center': (483, 513),
    'TOP-MIDDLE O Spot': (485, 552),
    'TOP-RIGHT Center': (607, 515),
    'TOP-RIGHT O Spot': (607, 551),
    'MIDDLE-LEFT Center': (364, 633),
    'MIDDLE-LEFT O Spot': (373, 667),
    'MIDDLE-MIDDLE Center': (483, 633),
    'MIDDLE-MIDDLE O Spot': (482, 668),
    'MIDDLE-RIGHT Center': (601, 633),
    'MIDDLE-RIGHT O Spot': (604, 666),
    'BOTTOM-LEFT Center': (368, 743),
    'BOTTOM-LEFT O Spot': (359, 773),
    'BOTTOM-MIDDLE Center': (482, 743),
    'BOTTOM-RIGHT Center': (599, 741),
    'BOTTOM-RIGHT O Spot': (598, 775)
}

# Define expected colors in RGB
EXPECTED_COLORS = {
    'TOP-LEFT Center': (141, 244, 255),
    'TOP-LEFT O Spot': (255, 163, 166),
    'TOP-MIDDLE Center': (141, 244, 255),
    'TOP-MIDDLE O Spot': (255, 164, 167),
    'TOP-RIGHT Center': (140, 244, 255),
    'TOP-RIGHT O Spot': (255, 160, 163),
    'MIDDLE-LEFT Center': (139, 243, 255),
    'MIDDLE-LEFT O Spot': (255, 164, 167),
    'MIDDLE-MIDDLE Center': (140, 244, 255),
    'MIDDLE-MIDDLE O Spot': (255, 163, 165),
    'MIDDLE-RIGHT Center': (138, 243, 255),
    'MIDDLE-RIGHT O Spot': (255, 157, 160),
    'BOTTOM-LEFT Center': (136, 242, 255),
    'BOTTOM-LEFT O Spot': (255, 153, 156),
    'BOTTOM-MIDDLE Center': (136, 242, 255),
    'BOTTOM-RIGHT Center': (134, 242, 255),
    'BOTTOM-RIGHT O Spot': (255, 153, 156)
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
    color = get_color_at_position(NEW_ROLE_POS)
    if color == COLOR_X:
        return 'X'
    elif color == COLOR_O:
        return 'O'
    return None

def check_squares():
    print("Checking the status of all squares...")
    for label, pos in SQUARE_POSITIONS.items():
        color = get_color_at_position(pos)
        expected_color = EXPECTED_COLORS.get(label)
        if color == expected_color:
            status = 'Correct'
        else:
            status = 'Incorrect'
        print(f"{label} Position: {pos}: RGB: {color}, Expected: {expected_color}, Status: {status}")

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
                # Check all squares on the Tic Tac Toe board
                check_squares()
                return  # Exit after determining the role and checking squares
            else:
                print("Waiting to determine if you are X or O...")
                time.sleep(1)  # Delay for a second before checking again

        else:
            if not was_party_empty:
                print("Player left. Waiting for a player to join the round...")
            was_party_empty = True  # Mark party as empty if not full
        
        time.sleep(1)  # Delay for a second before checking again

if __name__ == "__main__":
    main()
