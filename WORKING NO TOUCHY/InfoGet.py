import pyautogui
from PIL import ImageGrab
import keyboard

def get_color_at_cursor():
    # Get the current mouse position
    x, y = pyautogui.position()

    # Capture the screen at the mouse position
    screen = ImageGrab.grab()

    # Get the color of the pixel at the mouse position
    color = screen.getpixel((x, y))

    # Convert the color to hex format
    hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

    print(f"Position {x}, {y}: RGB: {color}, Hex: {hex_color}")

def main():
    print("Press CTRL to capture the color under the mouse cursor. Press ESC to exit.")

    # Run until 'ESC' is pressed
    while True:
        try:
            # Check if CTRL is pressed
            if keyboard.is_pressed('ctrl'):
                get_color_at_cursor()
                # Add a small delay to prevent multiple captures
                while keyboard.is_pressed('ctrl'):
                    pass  # Wait until the key is released

            # Check for ESC to exit
            if keyboard.is_pressed('esc'):
                print("Exiting...")
                break

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
