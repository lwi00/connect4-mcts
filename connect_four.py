from player import HumanPlayer, BotPlayer
from grid import Grid

class connect4: 
    def __init__(self, status=1):
        self.status = status
        self.grid = None
        self.players = [None, None]
        self.current_player_idx = 0

    def __str__(self):
        return f"Connect4 status={self.status})"

    def _launch_grid(self):
        try:
            self.grid = Grid()
        except Exception as e: 
            print(f"Grid initialization has failed: {e}")

    def _addPlayer(self, name, color, is_bot=False):
        if not is_bot:
            player = HumanPlayer(name, color)
        else:
            player = BotPlayer(name, color)
        if self.players[0] is None:
            self.players[0] = player
        elif self.players[1] is None:
            self.players[1] = player
        else:
            raise Exception("Both player slots are already filled.")

    def launch(self):
        print("Launching the game of connect 4...")
        self._launch_grid()
        # Add two human players for now
        while None in self.players:
            idx = self.players.index(None)
            name = input(f"Player {idx+1}, what is your name? ")
            color = 'red' if idx == 0 else 'yellow'
            self._addPlayer(name, color, is_bot=False)
        # Main game loop
        while not self.grid.is_game_over():
            self.grid.display_grid()
            current_player = self.players[self.current_player_idx]
            piece = self.current_player_idx + 1
            col = current_player.play(self.grid)
            try:
                self.grid.add_piece(col, piece)
            except ValueError as e:
                print(e)
                continue
            if self.grid.is_winner(piece):
                self.grid.display_grid()
                print(f"{current_player.name} ({current_player.color}) wins!")
                return
            if self.grid.is_draw():
                self.grid.display_grid()
                print("It's a draw!")
                return
            self.current_player_idx = 1 - self.current_player_idx


        