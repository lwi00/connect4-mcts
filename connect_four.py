from player import Player
from grid import Grid
class connect4: 
    def __init__(self, bot=0, status = 1):
        self
        self.bot = bot
        self.status = status
        self.grid= None,

    def __str__(self):
        return f"Connect4(bot={self.bot}, status={self.status})"


    def _launch_grid():
        grid = Grid.new_grid()
        
    
    def launch(self):
        print("Launching the game of connect 4...")
        self._launch_grid()
        