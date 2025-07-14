class Grid :
    def __init__(self, rows = 6, columns = 7):
        self.rows = rows
        self.columns = columns
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]

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
                return True
        
        raise ValueError("Column is full")