import random
from collections import deque
import tkinter as tk
from tkinter import messagebox

# Constants
GRID_SIZE = 10  # Size of the grid (10x10)
COLORS = ['red', 'green', 'blue', 'yellow', 'purple']  # Available colors
CELL_SIZE = 40  # Size of each grid cell (for visualization)

class ColorFloodGame:
    def __init__(self):
        # Initialize the game grid with random colors
        self.grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.steps = 0  # Counter for the number of moves made
        self.max_steps = 25  # Maximum number of moves allowed

    def flood_fill(self, x, y, target_color, replacement_color):
        """
        Perform a flood fill algorithm starting from (x, y).
        Replace all connected cells of the same color as target_color with replacement_color.
        """
        if target_color == replacement_color:
            return  # If target and replacement colors are the same, no changes are needed

        # Use a queue for breadth-first traversal
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()  # Get the current cell
            # Check if the cell is within bounds and matches the target color
            if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE and self.grid[cx][cy] == target_color:
                # Replace the color and add neighbors to the queue
                self.grid[cx][cy] = replacement_color
                queue.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])

    def make_move(self, color):
        """
        Make a move by flooding the grid starting from the top-left corner with the chosen color.
        """
        target_color = self.grid[0][0]  # The color at the top-left corner
        if target_color != color:  # Only proceed if the new color is different
            self.flood_fill(0, 0, target_color, color)
            self.steps += 1  # Increment the move counter

    def is_game_won(self):
        """
        Check if the game is won (i.e., all cells have the same color).
        """
        first_color = self.grid[0][0]
        return all(cell == first_color for row in self.grid for cell in row)


class ColorFloodGUI:
    def __init__(self, root):
        """
        Initialize the GUI for the game.
        """
        self.root = root
        self.root.title("Color Flood Game")
        self.game = ColorFloodGame()  # Create a game instance
        self.create_grid()  # Create the visual grid
        self.create_controls()  # Add control buttons
        self.create_status_bar()  # Add a status bar
        self.show_instructions()  # Show game instructions in a popup

    def show_instructions(self):
        """
        Display a message box with the game instructions.
        """
        messagebox.showinfo(
            "Welcome to Color Flood!",
            "Objective: Flood the grid with a single color within 25 moves.\n\n"
            "Instructions:\n"
            "- Select colors using the buttons below the grid.\n"
            "- The top-left corner and all connected cells of the same color will flood with the selected color.\n"
            "- Try to flood the entire grid in as few moves as possible.\n\n"
            "Press 'AI Move' to let the AI make a move.\n"
            "Press 'Reset' to start a new game.\n\nGood luck!"
        )

    def create_grid(self):
        """
        Create a grid of buttons representing the game grid.
        """
        self.buttons = []  # Store button references for updating colors
        self.grid_frame = tk.Frame(self.root)  # Frame to contain the grid
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10)

        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                # Create a button for each grid cell with the corresponding color
                btn = tk.Button(
                    self.grid_frame,
                    bg=self.game.grid[r][c],  # Initial background color
                    width=3,
                    height=1,
                    command=lambda color=self.game.grid[r][c]: self.make_move(color),  # On click, make a move
                )
                btn.grid(row=r, column=c, padx=1, pady=1)  # Place the button in the grid
                row.append(btn)
            self.buttons.append(row)

    def update_grid(self):
        """
        Update the colors of the grid buttons based on the game's current state.
        """
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.buttons[r][c].config(bg=self.game.grid[r][c])  # Update button color

    def create_controls(self):
        """
        Create control buttons for selecting colors, resetting the game, or making AI moves.
        """
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, pady=10)

        # Create a button for each color
        for color in COLORS:
            btn = tk.Button(
                self.control_frame,
                text=color.capitalize(),
                bg=color,  # Button background matches the color
                width=10,
                command=lambda color=color: self.make_move(color),  # On click, make a move
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Button for AI to make a move
        ai_button = tk.Button(
            self.control_frame,
            text="AI Move",
            bg="orange",
            width=10,
            command=self.ai_move,
        )
        ai_button.pack(side=tk.LEFT, padx=5)

        # Button to reset the game
        reset_button = tk.Button(
            self.control_frame,
            text="Reset",
            bg="gray",
            width=10,
            command=self.reset_game,
        )
        reset_button.pack(side=tk.LEFT, padx=5)

    def create_status_bar(self):
        """
        Create a status bar to display the number of moves and game status.
        """
        self.status_label = tk.Label(self.root, text="Steps: 0 / 25", font=("Arial", 12), anchor="w")
        self.status_label.grid(row=2, column=0, pady=10, sticky="w")

    def update_status(self):
        """
        Update the status bar with the current game status.
        """
        if self.game.is_game_won():
            self.status_label.config(text=f"Congratulations! You won in {self.game.steps} steps!")
        elif self.game.steps >= self.game.max_steps:
            self.status_label.config(text="Game Over! You ran out of moves.")
        else:
            self.status_label.config(text=f"Steps: {self.game.steps} / {self.game.max_steps}")

    def make_move(self, color):
        """
        Handle user moves, update the grid, and check the game status.
        """
        if self.game.is_game_won() or self.game.steps >= self.game.max_steps:
            return  # Ignore moves if the game is over
        self.game.make_move(color)  # Make the move in the game
        self.update_grid()  # Update the visual grid
        self.update_status()  # Update the status bar

    def ai_move(self):
        """
        Let the AI make a random move.
        """
        if not self.game.is_game_won() and self.game.steps < self.game.max_steps:
            color = random.choice(COLORS)  # Choose a random color
            self.make_move(color)

    def reset_game(self):
        """
        Reset the game to its initial state.
        """
        self.game = ColorFloodGame()  # Create a new game instance
        self.update_grid()  # Update the grid
        self.update_status()  # Reset the status bar

def main():
    """
    Entry point for the application.
    """
    root = tk.Tk()  # Create the main application window
    app = ColorFloodGUI(root)  # Initialize the GUI
    root.mainloop()  # Start the GUI event loop

if __name__ == "__main__":
    main()
