import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        root.title("MyApp")
        root.geometry("500x700")
        root.resizable(False, False)  # Make the window non-resizable

        # Create the status display label
        label_0 = tk.Label(root, text="Status: N/A", bg="#00aaff", fg="#000000", font=("Arial", 35))
        label_0.place(x=125, y=450, width=250, height=50)  # Adjusted position to be higher up

        # Create the tic-tac-toe board
        canvas = tk.Canvas(root, width=500, height=400)
        canvas.place(x=0, y=50)  # Position the board above the status box

        # Draw the tic-tac-toe grid
        canvas.create_line(167, 0, 167, 400, width=5)  # Vertical line 1
        canvas.create_line(333, 0, 333, 400, width=5)  # Vertical line 2
        canvas.create_line(0, 133, 500, 133, width=5)  # Horizontal line 1
        canvas.create_line(0, 267, 500, 267, width=5)  # Horizontal line 2

        # Create text labels for each square on the canvas
        squares = [
            (83.5, 66.5), (250, 66.5), (416.5, 66.5),  # Top row
            (83.5, 200), (250, 200), (416.5, 200),     # Middle row
            (83.5, 333.5), (250, 333.5), (416.5, 333.5)  # Bottom row
        ]

        for x, y in squares:
            canvas.create_text(x, y, text="  ", font=("Arial", 35))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
