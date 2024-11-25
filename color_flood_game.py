import random
from collections import deque
import tkinter as tk
from tkinter import messagebox

# Constants
GRID_SIZE = 10
COLORS = ['red', 'green', 'blue', 'yellow', 'purple']
CELL_SIZE = 40

class ColorFloodGame:
    def __init__(self):
        self.grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.steps = 0
        self.max_steps = 25  # Limit the number of moves

    def flood_fill(self, x, y, target_color, replacement_color):
        """Flood fill algorithm."""
        if target_color == replacement_color:
            return
        queue = deque([(x, y)])
        flooded_cells = 0
        while queue:
            cx, cy = queue.popleft()
            if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE and self.grid[cx][cy] == target_color:
                self.grid[cx][cy] = replacement_color
                flooded_cells += 1
                queue.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])
        return flooded_cells

    def make_move(self, color):
        """Perform a move by flooding the grid."""
        target_color = self.grid[0][0]
        if target_color != color:
            self.flood_fill(0, 0, target_color, color)
            self.steps += 1

    def is_game_won(self):
        """Check if all cells have the same color."""
        first_color = self.grid[0][0]
        return all(cell == first_color for row in self.grid for cell in row)

class ColorFloodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Flood Game")
        self.game = ColorFloodGame()
        self.create_grid()
        self.create_controls()
        self.create_status_bar()
        self.show_instructions()

    def show_instructions(self):
        """Show a popup with game instructions."""
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
        """Create the game grid in the GUI."""
        self.buttons = []
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10)

        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.grid_frame,
                    bg=self.game.grid[r][c],
                    width=3,
                    height=1,
                    command=lambda color=self.game.grid[r][c]: self.make_move(color),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)

    def update_grid(self):
        """Update the grid colors based on the game's state."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.buttons[r][c].config(bg=self.game.grid[r][c])

    def create_controls(self):
        """Create control buttons for the game."""
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, pady=10)

        for color in COLORS:
            btn = tk.Button(
                self.control_frame,
                text=color.capitalize(),
                bg=color,
                width=10,
                command=lambda color=color: self.make_move(color),
            )
            btn.pack(side=tk.LEFT, padx=5)

        ai_button = tk.Button(
            self.control_frame,
            text="AI Move",
            bg="orange",
            width=10,
            command=self.ai_move,
        )
        ai_button.pack(side=tk.LEFT, padx=5)

        reset_button = tk.Button(
            self.control_frame,
            text="Reset",
            bg="gray",
            width=10,
            command=self.reset_game,
        )
        reset_button.pack(side=tk.LEFT, padx=5)

    def create_status_bar(self):
        """Create a status bar to show game information."""
        self.status_label = tk.Label(self.root, text="Steps: 0 / 25", font=("Arial", 12), anchor="w")
        self.status_label.grid(row=2, column=0, pady=10, sticky="w")

    def update_status(self):
        """Update the status bar with current game status."""
        if self.game.is_game_won():
            self.status_label.config(text=f"Congratulations! You won in {self.game.steps} steps!")
        elif self.game.steps >= self.game.max_steps:
            self.status_label.config(text="Game Over! You ran out of moves.")
        else:
            self.status_label.config(text=f"Steps: {self.game.steps} / {self.game.max_steps}")

    def make_move(self, color):
        """Handle user moves."""
        if self.game.is_game_won() or self.game.steps >= self.game.max_steps:
            return
        self.game.make_move(color)
        self.update_grid()
        self.update_status()

    def ai_move(self):
        """Let the AI make a move using the Greedy Algorithm."""
        if not self.game.is_game_won() and self.game.steps < self.game.max_steps:
            best_color = None
            max_flooded_cells = -1

            # Evaluate each color for its potential impact on the grid
            for color in COLORS:
                # Make a copy of the current grid
                simulated_game = ColorFloodGame()
                simulated_game.grid = [row[:] for row in self.game.grid]
                simulated_game.make_move(color)

                # Count the number of flooded cells after the move
                flooded_cells = sum(row.count(simulated_game.grid[0][0]) for row in simulated_game.grid)

                # Choose the color that maximizes the number of flooded cells
                if flooded_cells > max_flooded_cells:
                    max_flooded_cells = flooded_cells
                    best_color = color

            # Perform the best move
            self.make_move(best_color)

    def reset_game(self):
        """Reset the game to its initial state."""
        self.game = ColorFloodGame()
        self.update_grid()
        self.update_status()

def main():
    root = tk.Tk()
    app = ColorFloodGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
