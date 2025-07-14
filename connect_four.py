from player import Player
from grid import Grid
class connect4: 
    def __init__(self,status = 1):
        self.status = status
        self.grid= None
        self.player = [None, None],

    def __str__(self):
        return f"Connect4 status={self.status})"


    def _launch_grid(self):
        try:
            self.grid = Grid.new_grid()
        except: 
            print("Grid initialization has failed")
        
        
    def _addPlayer(self, name):
        if self.player[0] is None:
            self.player[0] = Player.new_player(name, 'red')
        elif self.player[1] is None:
            self.player[1] = Player.new_player(name, 'yellow')
        else:
            raise Exception("Both player slots are already filled.")

    def launch(self):
        print("Launching the game of connect 4...")
        self._launch_grid()
        while None in self.player:
            self._addPlayer(input("what is your name ?"))


        