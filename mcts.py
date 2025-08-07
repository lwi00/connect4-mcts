import random
import math
from node import Node
from grid import Grid

class MCTS:
    def __init__(self, exploration_constant=1.414):
        self.exploration_constant = exploration_constant
    
    def find_immediate_win(self, grid, player):
        """Find immediate winning move for a player"""
        valid_moves = grid.get_valid_moves()
        for move in valid_moves:
            # Create a copy and test the move
            test_grid = Grid()
            test_grid.grid = [row[:] for row in grid.grid]
            test_grid.current_player_idx = grid.current_player_idx
            
            try:
                test_grid.add_piece(move, player)
                if test_grid.is_winner(player):
                    return move
            except ValueError:
                continue
        return None
    
    def find_immediate_block(self, grid, opponent):
        """Find move to block opponent's immediate win"""
        return self.find_immediate_win(grid, opponent)
    
    def get_priority_move(self, grid):
        """Get highest priority move (win > block > MCTS)"""
        current_player = grid.get_current_player()
        opponent = 3 - current_player  # 1->2, 2->1
        
        # Check for immediate win
        winning_move = self.find_immediate_win(grid, current_player)
        if winning_move is not None:
            return winning_move
        
        # Check for immediate block
        blocking_move = self.find_immediate_block(grid, opponent)
        if blocking_move is not None:
            return blocking_move
        
        # No immediate win/block, use MCTS
        return None

    def ucb1(self, node, parent_visits):
        """Calculate UCB1 value for node selection"""
        if node.visit == 0:
            return float('inf')
        
        if parent_visits == 0:
            return float('inf')
        
        exploitation = node.total_victory / node.visit
        exploration = self.exploration_constant * math.sqrt(math.log(parent_visits) / node.visit)
        return exploitation + exploration
    
    def select(self, node):
        """Selection phase: traverse tree using UCB1 until we reach a leaf node"""
        while not node.is_terminal() and node.is_fully_expanded():
            # Find child with highest UCB1 value
            best_child = None
            best_ucb1 = float('-inf')
            
            for child in node.children:
                ucb1_value = self.ucb1(child, node.visit)
                if ucb1_value > best_ucb1:
                    best_ucb1 = ucb1_value
                    best_child = child
            
            node = best_child
        
        return node
    
    def expand(self, node):
        """Expansion phase: create one new child node"""
        if node.is_terminal():
            return node
        
        # Expand the node if not already expanded
        if not node.is_expanded:
            node.expand()
        
        # Return an unvisited child if available
        for child in node.children:
            if child.visit == 0:
                return child
        
        # If all children have been visited, return the node itself
        return node
    
    def simulate(self, node):
        """Simulation phase: play random moves until game ends"""
        if node.is_terminal():
            return self._get_game_result(node.state)
        
        # Create a copy of the state for simulation
        simulation_state = node.state
        while not simulation_state.is_game_over():
            valid_moves = simulation_state.get_valid_moves()
            if not valid_moves:
                break
            
            # Make a random move
            move = random.choice(valid_moves)
            current_player = simulation_state.get_current_player()
            simulation_state.add_piece(move, current_player)
        
        return self._get_game_result(simulation_state)
    
    def backpropagate(self, node, result):
        """Backpropagation phase: update statistics up the tree"""
        while node is not None:
            node.visit += 1
            
            # Update win count for the player who made the move to this node
            if result == "victory":
                node.total_victory += 1
            elif result == "defeat":
                node.total_defeat += 1
            elif result == "draw":
                node.total_draw += 1
            
            # Update UCB1 value
            if node.parent:
                node.ucb1 = self.ucb1(node, node.parent.visit)
            
            node = node.parent
    
    def _get_game_result(self, state):
        """Determine game result from the perspective of the current player"""
        if state.is_winner(1):
            return "victory" if state.current_player_idx == 0 else "defeat"
        elif state.is_winner(2):
            return "victory" if state.current_player_idx == 1 else "defeat"
        else:
            return "draw"
    
    def run_mcts(self, root_state, iterations=1000):
        """Run MCTS algorithm and return the best move"""
        # Check if there are any valid moves
        valid_moves = root_state.get_valid_moves()
        if not valid_moves:
            return None
        
        # Check for priority moves (win/block) first
        priority_move = self.get_priority_move(root_state)
        if priority_move is not None:
            return priority_move
        
        # Create root node
        root = Node(root_state)
        
        # Run MCTS iterations
        for _ in range(iterations):
            # Selection
            leaf = self.select(root)
            
            # Expansion
            new_node = self.expand(leaf)
            
            # Simulation
            result = self.simulate(new_node)
            
            # Backpropagation
            self.backpropagate(new_node, result)
        
        # Return the move with highest visit count
        if not root.children:
            return None
        
        best_child = max(root.children, key=lambda child: child.visit)
        return best_child.move

def get_best_move(grid, iterations=1000):
    """Convenience function to get the best move for a given grid state"""
    mcts = MCTS()
    return mcts.run_mcts(grid, iterations)


