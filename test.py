import time
from PIL import ImageGrab
import threading
import keyboard  # For detecting key presses

# Define positions for the Tic Tac Toe board
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

# Define acceptable shades of colors
ACCEPTABLE_COLORS = {
    'blue': [(141, 244, 255), (140, 244, 255), (139, 243, 255), (136, 242, 255), (134, 242, 255)],
    'red': [(255, 163, 166), (255, 164, 167), (255, 160, 163), (255, 157, 160), (255, 153, 156)]
}

def get_color_at_position(image, position):
    x, y = position
    return image.getpixel((x, y))

def is_color_acceptable(color):
    return color in [color for colors in ACCEPTABLE_COLORS.values() for color in colors]

def check_squares(image, prev_states):
    radius = 5  # Radius around the point to check
    statuses = {}
    
    for label, pos in SQUARE_POSITIONS.items():
        x, y = pos
        correct = False
        
        # Check a 5-pixel radius around the point
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                current_pos = (x + dx, y + dy)
                color = get_color_at_position(image, current_pos)
                if is_color_acceptable(color):
                    correct = True
                    break
            if correct:
                break
        
        status = 'Correct' if correct else 'Incorrect'
        statuses[label] = status
    
    return statuses

def monitor_keyboard(stop_event):
    print("Press ESC to exit.")
    keyboard.wait('esc')  # Wait until the ESC key is pressed
    stop_event.set()  # Signal to stop the main loop

def main():
    prev_states = {label: 'Unknown' for label in SQUARE_POSITIONS.keys()}
    print("Starting checks...")

    stop_event = threading.Event()

    # Start a separate thread to monitor keyboard input
    keyboard_thread = threading.Thread(target=monitor_keyboard, args=(stop_event,))
    keyboard_thread.start()

    while not stop_event.is_set():
        # Capture the screen once per cycle
        screen = ImageGrab.grab()
        # Check all squares in the captured image
        current_states = check_squares(screen, prev_states)

        # Print status updates for any changes
        for label, status in current_states.items():
            if prev_states[label] != status:
                prev_states[label] = status
                print(f"{label} Position: {SQUARE_POSITIONS[label]}: Status: {status}")

        # Delay for a short interval before the next check
        time.sleep(0.5)  # Adjust this delay to control how frequently the checks are performed

    print("Exiting...")

if __name__ == "__main__":
    main()
