class Grid :
    def __init__(self, rows = 6, columns = 7):
        pass
        self.rows = rows
        self.columns = columns
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]

    def new_grid(self):
        return Grid()
    
    def display_grid(self):
        for i in self.grid: 
            print(i)