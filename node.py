class Node:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.parent = None
        self.is_leaf = False
        self.is_root = False
        self.total_weight = 0
        self.total_victory = 0
        self.total_defeat = 0
        self.total_draw = 0

    def __str__(self):
        return f"Node(state={self.state})"
    def expand(self):
        pass
    def back_propagate(self, result):
        pass

class CurrentNode(Node):
    def __init__(self, value):
        super().__init__(value)
        self.is_leaf = True
        self.is_root = False
        self.total_weight = 0
        self.total_victory = 0
    
