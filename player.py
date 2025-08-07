from mcts import get_best_move

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def __str__(self):
        return f"{self.name} ({self.color})"

class HumanPlayer(Player):
    def __init__(self, name, color):
        super().__init__(name, color)

    def play(self, grid):
        while True:
            try:
                col = int(input(f"{self.name} ({self.color}), choose a column (0-{grid.columns-1}): "))
                if col in grid.get_valid_moves():
                    return col
                else:
                    print("Column is full or invalid. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

class BotPlayer(Player):
    def __init__(self, name, color, iterations=1000):
        super().__init__(name, color)
        self.iterations = iterations
    
    def play(self, grid):
        print(f"{self.name} ({self.color}) is thinking...")
        best_move = get_best_move(grid, self.iterations)
        print(f"{self.name} chooses column {best_move}")
        return best_move
    