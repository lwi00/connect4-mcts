import numpy as np

class Node:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.parent = None
        self.is_leaf = False
        self.is_root = False
        self.visit = 0
        self.total_victory = 0
        self.total_defeat = 0
        self.total_draw = 0
        self.ucb1 = 0
        self.move = None
        self.is_expanded = False
        
    def __str__(self):
        return f"Node(state={self.state})"
    def expand(self):
        pass
            
    def back_propagate(self, result):
        self.total_visit += 1
        if result == "victory":
            self.total_victory += 1
        elif result == "defeat":
            self.total_defeat += 1
        elif result == "draw":
            self.total_draw += 1
        if self.parent:
            self.parent.back_propagate(result)
    def is_leaf(self):
        return len(self.children) == 0
    def is_root(self):
        return self.parent is None
    def is_terminal(self):
        return self.is_leaf() or self.is_root()
    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())
    
    def get_best_child(self):
        return max(self.children, key=lambda child: child.ucb1)
    
    def get_ucb1(self):
        return self.total_victory / self.total_visit + np.sqrt(2 * np.log(self.parent.total_visit) / self.total_visit)
    
    def update_ucb1(self):
        self.ucb1 = self.get_ucb1()