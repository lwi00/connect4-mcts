class Player:
    def __init__(self, name, color ):
        self.name = name
        self.color = color
    
    def __str__(self):
        return f"{self.name} ({self.color})"

    def new_player():
        name = input("Name of the player : ")
        color = input("Color of your player : ")
        return Player(name, color)
