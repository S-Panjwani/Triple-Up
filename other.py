import pyautogui
from PIL import ImageGrab
import time

# Function to check the color at a specific position
def check_color(x, y, expected_rgb):
    screenshot = ImageGrab.grab()
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color == expected_rgb

# Coordinates and RGB values
positions = [
    (1030, 166, (0, 0, 0)),
    (1024, 163, (0, 0, 0)),
    (1035, 160, (0, 0, 0))
]

# Continuously check colors and click if all match
while True:
    # Get the current mouse position
    original_position = pyautogui.position()

    # Check if all colors match
    all_match = all(check_color(x, y, rgb) for x, y, rgb in positions)

    if all_match:
        for x, y, _ in positions:
            # Move to the position
            pyautogui.moveTo(x, y)
            time.sleep(0.1)  # Short delay for stability

            # Perform a manual mouse click (mouse down and up)
            pyautogui.mouseDown()
            time.sleep(0.05)  # Slight pause between down and up
            pyautogui.mouseUp()

        # Return mouse to its original position
        pyautogui.moveTo(original_position)
        time.sleep(0.1)  # Short delay to ensure the mouse movement is smooth

    time.sleep(0.5)  # Longer delay to reduce system load
