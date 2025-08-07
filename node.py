import numpy as np
import copy

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
        """Expand the node by creating child nodes for all valid moves"""
        if self.is_expanded:
            return
        
        valid_moves = self.state.get_valid_moves()
        current_player = 1 if self.state.current_player_idx == 0 else 2
        
        for move in valid_moves:
            # Create a deep copy of the current state
            new_state = copy.deepcopy(self.state)
            
            # Make the move
            try:
                new_state.add_piece(move, current_player)
                new_state.current_player_idx = 1 - new_state.current_player_idx
                
                # Create child node
                child = Node(new_state)
                child.parent = self
                child.move = move
                child.is_leaf = new_state.is_game_over()
                
                self.children.append(child)
            except ValueError:
                # Skip invalid moves
                continue
        
        self.is_expanded = True
            
    def back_propagate(self, result):
        self.visit += 1
        if result == "victory":
            self.total_victory += 1
        elif result == "defeat":
            self.total_defeat += 1
        elif result == "draw":
            self.total_draw += 1
        if self.parent:
            self.parent.back_propagate(result)
    
    def is_leaf_node(self):
        return len(self.children) == 0
    
    def is_root_node(self):
        return self.parent is None
    
    def is_terminal(self):
        return self.state.is_game_over()
    
    def is_fully_expanded(self):
        return self.is_expanded and len(self.children) == len(self.state.get_valid_moves())
    
    def get_best_child(self):
        return max(self.children, key=lambda child: child.ucb1)
    
    def get_ucb1(self):
        if self.visit == 0:
            return float('inf')
        if self.parent is None:
            return 0
        return self.total_victory / self.visit + np.sqrt(2 * np.log(self.parent.visit) / self.visit)
    
    def update_ucb1(self):
        self.ucb1 = self.get_ucb1()