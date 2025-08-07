class Grid :
    def __init__(self, rows = 6, columns = 7):
        self.rows = rows
        self.columns = columns
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.current_player_idx = 0  # 0 for player 1, 1 for player 2

    def new_grid():
        return Grid()
    
    def display_grid(self):
        for i in self.grid: 
            print(i)
    
    def add_piece(self, column, piece):
        if column < 0 or column >= self.columns:
            raise ValueError("Column index out of bounds")
        
        for row in reversed(range(self.rows)):
            if self.grid[row][column] == 0:
                self.grid[row][column] = piece
                # Switch to next player
                self.current_player_idx = 1 - self.current_player_idx
                return True
        
        raise ValueError("Column is full")
    
    def get_current_player(self):
        """Returns the current player number (1 or 2)"""
        return self.current_player_idx + 1
    
    def set_current_player(self, player_idx):
        """Set the current player (0 for player 1, 1 for player 2)"""
        self.current_player_idx = player_idx
    
    def is_full(self):
        return all(cell != 0 for row in self.grid for cell in row)
    
    def is_winner(self, piece):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(self.grid[row][col + i] == piece for i in range(4)):
                    return True
                
        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.columns):
                if all(self.grid[row + i][col] == piece for i in range(4)):
                    return True
                    
        # Check diagonal (down-right)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.grid[row + i][col + i] == piece for i in range(4)):
                    return True
                    
        # Check diagonal (down-left)
        for row in range(self.rows - 3):
            for col in range(3, self.columns):
                if all(self.grid[row + i][col - i] == piece for i in range(4)):
                    return True
                    
        return False
    
    def is_draw(self):
        return self.is_full() and not self.is_winner(1) and not self.is_winner(2)
    
    def is_game_over(self):
        return self.is_winner(1) or self.is_winner(2) or self.is_draw()
    
    def get_valid_moves(self):
        return [i for i in range(self.columns) if self.grid[0][i] == 0]
