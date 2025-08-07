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

    def _addPlayer(self, name, color, is_bot=False, iterations=1000):
        if not is_bot:
            player = HumanPlayer(name, color)
        else:
            player = BotPlayer(name, color, iterations)
        if self.players[0] is None:
            self.players[0] = player
        elif self.players[1] is None:
            self.players[1] = player
        else:
            raise Exception("Both player slots are already filled.")

    def _choose_game_mode(self):
        print("\nChoose game mode:")
        print("1. Human vs Human")
        print("2. Human vs AI")
        print("3. AI vs AI")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if choice in [1, 2, 3]:
                    return choice
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")

    def launch(self):
        print("Launching the game of connect 4...")
        self._launch_grid()
        
        # Choose game mode
        game_mode = self._choose_game_mode()
        
        # Set up players based on game mode
        if game_mode == 1:  # Human vs Human
            for i in range(2):
                name = input(f"Player {i+1}, what is your name? ")
                color = 'red' if i == 0 else 'yellow'
                self._addPlayer(name, color, is_bot=False)
        
        elif game_mode == 2:  # Human vs AI
            human_name = input("Human player, what is your name? ")
            self._addPlayer(human_name, 'red', is_bot=False)
            self._addPlayer("AI", 'yellow', is_bot=True, iterations=1000)
        
        elif game_mode == 3:  # AI vs AI
            self._addPlayer("AI 1", 'red', is_bot=True, iterations=1000)
            self._addPlayer("AI 2", 'yellow', is_bot=True, iterations=1000)
        
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


        