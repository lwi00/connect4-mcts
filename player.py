class Player:
    def __init__(self, name, color, bot = 0 ):
        self.name = name
        self.color = color
        self.bot = 0,
    
    def __str__(self):
        return f"{self.name} ({self.color})"

    def new_player(name, color, is_bot = 0):
        return Player(name, color, is_bot)

