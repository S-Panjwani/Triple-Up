import time
import numpy as np
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor
import threading  # Import threading module
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

# Convert acceptable colors to a set for faster lookups
ACCEPTABLE_COLOR_SET = set(tuple(c) for color_list in ACCEPTABLE_COLORS.values() for c in color_list)

def get_color_at_position(position, screen_array):
    x, y = position
    return tuple(screen_array[y, x])

def is_color_acceptable(color):
    return color in ACCEPTABLE_COLOR_SET

def check_square(label, pos, prev_states, screen_array):
    x, y = pos
    radius = 5  # Radius around the point to check
    correct = False
    
    # Check a 5-pixel radius around the point
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            current_pos = (x + dx, y + dy)
            if 0 <= current_pos[0] < screen_array.shape[1] and 0 <= current_pos[1] < screen_array.shape[0]:
                color = get_color_at_position(current_pos, screen_array)
                if is_color_acceptable(color):
                    correct = True
                    break
        if correct:
            break
    
    status = 'Correct' if correct else 'Incorrect'
    
    # Only print if the status has changed
    if prev_states[label] != status:
        prev_states[label] = status
        print(f"{label} Position: {pos}: Status: {status}")

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
        screen = ImageGrab.grab()
        screen_array = np.array(screen)

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(check_square, label, pos, prev_states, screen_array)
                for label, pos in SQUARE_POSITIONS.items()
            ]
            for future in futures:
                future.result()  # Ensure each future completes

        # Delay for a short interval before the next check
        time.sleep(0.1)  # Adjust this delay to control how frequently the checks are performed

    print("Exiting...")

if __name__ == "__main__":
    main()
