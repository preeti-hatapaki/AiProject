import random
from collections import deque
import tkinter as tk
from tkinter import messagebox

print("""
Welcome to the Color Flood Game!

Objective: Flood the grid with a single color within 25 moves.

Instructions:
- Select colors using the buttons below the grid.
- The top-left corner and all connected cells of the same color will flood with the selected color.
- Try to flood the entire grid in as few moves as possible.

You can also let the AI make moves by clicking the "AI Move" button.
Press "Reset" to start a new game.

Good luck!
""")
messagebox.showinfo(
    "Welcome to Color Flood!",
    "Objective: Flood the grid with a single color within 25 moves.\n\n"
    "Instructions:\n"
    "- Select colors using the buttons below the grid.\n"
    "- The top-left corner and all connected cells of the same color will flood with the selected color.\n"
    "- Try to flood the entire grid in as few moves as possible.\n\n"
    "You can also let the AI make moves by clicking the 'AI Move' button.\n"
    "Press 'Reset' to start a new game.\n\nGood luck!"
)

# Constants
GRID_SIZE = 10
COLORS = ['red', 'green', 'blue', 'yellow', 'purple']
CELL_SIZE = 40

class ColorFloodGame:
    def __init__(self):
        self.grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.steps = 0
        self.max_steps = 25  # Limit the number of moves
        self.ai_mode = False

    def flood_fill(self, x, y, target_color, replacement_color):
        """Flood fill algorithm."""
        if target_color == replacement_color:
            return
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE and self.grid[cx][cy] == target_color:
                self.grid[cx][cy] = replacement_color
                queue.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])

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

class ColorFloodAI:
    def __init__(self, game):
        self.game = game

    def calculate_area(self, x, y, color):
        """Calculate the size of the connected area for a given color."""
        visited = set()
        queue = deque([(x, y)])
        area_size = 0
        target_color = self.game.grid[x][y]

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) not in visited and 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE:
                if self.game.grid[cx][cy] == target_color or self.game.grid[cx][cy] == color:
                    visited.add((cx, cy))
                    area_size += 1
                    queue.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])

        return area_size

    def select_best_move(self):
        """Select the color that results in the largest flooded area."""
        target_color = self.game.grid[0][0]
        max_area = 0
        best_color = target_color

        for color in COLORS:
            if color != target_color:
                area = self.calculate_area(0, 0, color)
                if area > max_area:
                    max_area = area
                    best_color = color

        return best_color

class ColorFloodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Flood Game")
        self.game = ColorFloodGame()
        self.ai = ColorFloodAI(self.game)
        self.buttons = []
        self.create_grid()
        self.create_controls()

    def create_grid(self):
        """Create the game grid in the GUI."""
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.root, 
                    bg=self.game.grid[r][c],
                    width=2, 
                    height=1,
                    command=lambda color=self.game.grid[r][c]: self.make_move(color)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)

    def update_grid(self):
        """Update the grid colors based on the game's state."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.buttons[r][c].config(bg=self.game.grid[r][c])

    def make_move(self, color):
        """Handle user moves."""
        if self.game.is_game_won() or self.game.steps >= self.game.max_steps:
            messagebox.showinfo("Game Over", "The game is over!")
            return
        self.game.make_move(color)
        self.update_grid()

        if self.game.is_game_won():
            messagebox.showinfo("Congratulations!", f"You won in {self.game.steps} steps!")
        elif self.game.steps >= self.game.max_steps:
            messagebox.showinfo("Game Over", "You lost. Try again!")

    def ai_move(self):
        """Let the AI make a move."""
        if not self.game.is_game_won() and self.game.steps < self.game.max_steps:
            best_move = self.ai.select_best_move()
            self.make_move(best_move)

    def create_controls(self):
        """Create control buttons for the game."""
        frame = tk.Frame(self.root)
        frame.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE)

        for color in COLORS:
            btn = tk.Button(
                frame, text=color, bg=color, width=8, command=lambda color=color: self.make_move(color)
            )
            btn.pack(side=tk.LEFT, padx=5)

        ai_button = tk.Button(frame, text="AI Move", command=self.ai_move)
        ai_button.pack(side=tk.LEFT, padx=5)

        reset_button = tk.Button(frame, text="Reset", command=self.reset_game)
        reset_button.pack(side=tk.LEFT, padx=5)

    def reset_game(self):
        """Reset the game to its initial state."""
        self.game = ColorFloodGame()
        self.ai = ColorFloodAI(self.game)
        self.update_grid()

def main():
    root = tk.Tk()
    app = ColorFloodGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
