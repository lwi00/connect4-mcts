# Connect 4 with MCTS - Technical Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [MCTS Algorithm](#mcts-algorithm)
5. [Game Flow](#game-flow)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Performance Considerations](#performance-considerations)

---

## Project Overview

This is a Python implementation of the classic Connect 4 game featuring an AI opponent powered by Monte Carlo Tree Search (MCTS). The project demonstrates object-oriented design principles, game tree search algorithms, and comprehensive testing practices.

### Key Features
- Multiple game modes (Human vs Human, Human vs AI, AI vs AI)
- MCTS-based AI with configurable difficulty
- Immediate win/block detection for optimal play
- UCB1 (Upper Confidence Bound) for balanced exploration-exploitation
- Clean separation of concerns with modular architecture
- Comprehensive test coverage

---

## Architecture

The project follows a modular object-oriented architecture with clear separation of concerns:

```
┌─────────────┐
│   main.py   │  Entry point
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ connect_four.py │  Game orchestration
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌──────┐ ┌────────┐ ┌────────┐ ┌───────┐
│grid.py│ │player.py│ │mcts.py│ │node.py│
└──────┘ └────────┘ └───┬────┘ └───────┘
                        │
                        └─── Uses Node
```

---

## Core Components

### 1. Grid (`grid.py`)

The `Grid` class represents the Connect 4 game board and implements all game rules.

**Attributes:**
- `rows`: Number of rows (default: 6)
- `columns`: Number of columns (default: 7)
- `grid`: 2D list representing the board state
- `current_player_idx`: Index of current player (0 or 1)

**Key Methods:**

#### `add_piece(column, piece)`
Adds a piece to the specified column using gravity simulation.
- **Parameters:**
  - `column` (int): Column index (0-6)
  - `piece` (int): Player piece (1 or 2)
- **Returns:** `True` on success
- **Raises:** `ValueError` if column is full or out of bounds
- **Location:** `grid.py:15`

#### `is_winner(piece)`
Checks if the specified piece has won the game by checking all four directions (horizontal, vertical, two diagonals).
- **Parameters:**
  - `piece` (int): Player piece to check (1 or 2)
- **Returns:** `bool` indicating if player has won
- **Location:** `grid.py:39`

#### `get_valid_moves()`
Returns list of columns that are not full.
- **Returns:** List of valid column indices
- **Location:** `grid.py:72`

#### `is_game_over()`
Checks if game has ended (win or draw).
- **Returns:** `bool` indicating if game is over
- **Location:** `grid.py:69`

---

### 2. Player Classes (`player.py`)

Abstract base class `Player` with two concrete implementations:

#### `HumanPlayer`
Interactive player that reads moves from command line input.

**Method:**
- `play(grid)`: Prompts user for column input and validates it
- **Location:** `player.py:15`

#### `BotPlayer`
AI player using MCTS algorithm.

**Attributes:**
- `iterations`: Number of MCTS iterations (controls AI strength)

**Method:**
- `play(grid)`: Computes best move using MCTS
- **Location:** `player.py:31`

---

### 3. MCTS Implementation (`mcts.py`)

The MCTS class implements the Monte Carlo Tree Search algorithm with four phases.

#### Key Methods:

##### `run_mcts(root_state, iterations=1000)`
Main entry point that executes the full MCTS algorithm.
- **Parameters:**
  - `root_state`: Current grid state
  - `iterations`: Number of search iterations
- **Returns:** Best column to play
- **Location:** `mcts.py:142`

##### `select(node)`
**Selection Phase**: Traverses tree using UCB1 until reaching an unexpanded node.
- Uses UCB1 formula: `exploitation + exploration`
- **Location:** `mcts.py:61`

##### `expand(node)`
**Expansion Phase**: Creates child nodes for all valid moves from current position.
- **Location:** `mcts.py:78`

##### `simulate(node)`
**Simulation Phase**: Plays out game randomly from current position to terminal state.
- **Location:** `mcts.py:95`

##### `backpropagate(node, result)`
**Backpropagation Phase**: Updates statistics (visits, wins) up the tree.
- **Location:** `mcts.py:114`

#### Priority Move Detection

##### `get_priority_move(grid)`
Implements tactical awareness before running full MCTS:
1. Check for immediate winning move
2. Check for opponent's winning move to block
3. Fall back to MCTS if no urgent moves

**Location:** `mcts.py:31`

This optimization significantly improves play quality and reduces computation time for tactical positions.

---

### 4. Node Class (`node.py`)

Represents a node in the MCTS game tree.

**Attributes:**
- `state`: Grid state at this node
- `children`: List of child nodes
- `parent`: Parent node reference
- `visit`: Number of times node has been visited
- `total_victory`: Count of simulations that resulted in victory
- `total_defeat`: Count of simulations that resulted in defeat
- `total_draw`: Count of simulations that resulted in draw
- `ucb1`: UCB1 value for selection
- `move`: The move that led to this node
- `is_expanded`: Whether children have been created

**Key Methods:**

##### `expand()`
Creates child nodes for all valid moves from current state.
- Deep copies state for each child
- Marks terminal nodes appropriately
- **Location:** `node.py:22`

##### `get_ucb1()`
Calculates UCB1 value: `win_rate + c * sqrt(ln(parent_visits) / visits)`
- Returns infinity for unvisited nodes (ensures exploration)
- **Location:** `node.py:78`

##### `back_propagate(result)`
Recursively updates statistics up to root.
- **Location:** `node.py:52`

---

### 5. Game Controller (`connect_four.py`)

The `connect4` class orchestrates the game flow.

**Key Methods:**

##### `_choose_game_mode()`
Interactive menu for selecting game mode.
- **Location:** `connect_four.py:32`

##### `_addPlayer(name, color, is_bot, iterations)`
Creates and registers a player.
- **Location:** `connect_four.py:20`

##### `launch()`
Main game loop:
1. Initialize grid
2. Set up players based on mode
3. Execute turn-based gameplay
4. Handle win/draw conditions

**Location:** `connect_four.py:48`

---

## MCTS Algorithm

### Overview

Monte Carlo Tree Search is a best-first search algorithm that builds a game tree incrementally. It balances exploration (trying new moves) with exploitation (focusing on promising moves).

### Four Phases

#### 1. Selection
Starting from root, recursively select child with highest UCB1 value until reaching a leaf node or terminal state.

**UCB1 Formula:**
```
UCB1 = (wins / visits) + c * sqrt(ln(parent_visits) / visits)
```
- First term: Exploitation (win rate)
- Second term: Exploration (uncertainty bonus)
- `c`: Exploration constant (default: 1.414 = sqrt(2))

#### 2. Expansion
Create child nodes for all legal moves from the selected node.

#### 3. Simulation (Rollout)
From the expanded node, play random moves until reaching a terminal state. Record the outcome.

#### 4. Backpropagation
Update visit counts and win statistics for all nodes from the simulated node back to the root.

### Optimizations

#### Immediate Win/Block Detection
Before running MCTS iterations, check for:
1. **Winning moves**: If current player can win immediately, play that move
2. **Blocking moves**: If opponent can win next turn, block them

This tactical layer prevents the AI from missing obvious moves and dramatically improves play quality.

#### Visit-Count Selection
After all iterations, select the child of root with highest visit count (not highest win rate). This is more robust as it's less susceptible to variance.

---

## Game Flow

### Initialization Sequence

1. `main.py` creates a `connect4` instance
2. `connect4.launch()` is called:
   - Grid is initialized (6x7 board)
   - User selects game mode
   - Players are created based on mode
   - Game loop begins

### Turn Execution

```python
while not grid.is_game_over():
    1. Display current board state
    2. Get move from current player
       - HumanPlayer: Read from input
       - BotPlayer: Run MCTS algorithm
    3. Validate and apply move to grid
    4. Check for win condition
    5. Check for draw condition
    6. Switch to other player
```

### AI Decision Making

When a `BotPlayer` is asked to play:
1. Call `get_best_move(grid, iterations)`
2. MCTS checks for priority moves (win/block)
3. If no priority move, build search tree:
   - Run 1000 iterations (default)
   - Each iteration: select → expand → simulate → backpropagate
4. Return move with highest visit count
5. Column number is passed to grid

---

## API Reference

### Grid Class

```python
class Grid:
    def __init__(self, rows=6, columns=7)
    def display_grid(self) -> None
    def add_piece(self, column: int, piece: int) -> bool
    def get_current_player(self) -> int
    def set_current_player(self, player_idx: int) -> None
    def is_full(self) -> bool
    def is_winner(self, piece: int) -> bool
    def is_draw(self) -> bool
    def is_game_over(self) -> bool
    def get_valid_moves(self) -> List[int]
```

### Player Classes

```python
class Player:
    def __init__(self, name: str, color: str)
    def play(self, grid: Grid) -> int  # Abstract

class HumanPlayer(Player):
    def play(self, grid: Grid) -> int

class BotPlayer(Player):
    def __init__(self, name: str, color: str, iterations: int = 1000)
    def play(self, grid: Grid) -> int
```

### MCTS Class

```python
class MCTS:
    def __init__(self, exploration_constant: float = 1.414)
    def find_immediate_win(self, grid: Grid, player: int) -> Optional[int]
    def find_immediate_block(self, grid: Grid, opponent: int) -> Optional[int]
    def get_priority_move(self, grid: Grid) -> Optional[int]
    def ucb1(self, node: Node, parent_visits: int) -> float
    def select(self, node: Node) -> Node
    def expand(self, node: Node) -> Node
    def simulate(self, node: Node) -> str
    def backpropagate(self, node: Node, result: str) -> None
    def run_mcts(self, root_state: Grid, iterations: int = 1000) -> Optional[int]
```

### Node Class

```python
class Node:
    def __init__(self, state: Grid)
    def expand(self) -> None
    def back_propagate(self, result: str) -> None
    def is_leaf_node(self) -> bool
    def is_root_node(self) -> bool
    def is_terminal(self) -> bool
    def is_fully_expanded(self) -> bool
    def get_best_child(self) -> Node
    def get_ucb1(self) -> float
    def update_ucb1(self) -> None
```

### Connect4 Game Class

```python
class connect4:
    def __init__(self, status: int = 1)
    def _launch_grid(self) -> None
    def _addPlayer(self, name: str, color: str, is_bot: bool = False,
                   iterations: int = 1000) -> None
    def _choose_game_mode(self) -> int
    def launch(self) -> None
```

---

## Testing

The test suite (`test_connect4.py`) provides comprehensive coverage:

### Grid Tests
- `test_add_piece_and_valid_moves()`: Piece placement and column validation
- `test_horizontal_win()`: Horizontal win detection
- `test_vertical_win()`: Vertical win detection
- `test_diagonal_win()`: Diagonal win detection
- `test_draw()`: Draw condition detection

### MCTS Tests
- `test_mcts_returns_valid_move()`: Basic validity check
- `test_mcts_with_winning_move()`: Winning move detection
- `test_mcts_with_full_column()`: Handling full columns
- `test_mcts_finds_immediate_win()`: Priority move detection
- `test_mcts_blocks_immediate_loss()`: Defensive play
- `test_priority_move_detection()`: Win/block logic

### Bot Player Tests
- `test_botplayer_move_is_valid()`: AI move validity

### Running Tests

```bash
# Run all tests
pytest test_connect4.py

# Run with verbose output
pytest test_connect4.py -v

# Run specific test
pytest test_connect4.py::test_mcts_finds_immediate_win
```

---

## Performance Considerations

### MCTS Iterations

The number of MCTS iterations directly impacts:
- **AI Strength**: More iterations = better moves
- **Response Time**: More iterations = longer wait

**Recommended Settings:**
- Easy AI: 100-500 iterations (~0.1-0.5 seconds)
- Medium AI: 1000-2000 iterations (~1-2 seconds)
- Hard AI: 5000-10000 iterations (~5-10 seconds)

### Memory Usage

Each MCTS iteration creates nodes in memory. For a typical game:
- Node size: ~200 bytes
- 1000 iterations: ~200 KB
- 10000 iterations: ~2 MB

Memory is released after each move, so total usage remains manageable.

### Optimization Opportunities

1. **Transposition Tables**: Cache previously evaluated positions
2. **Parallel MCTS**: Run simulations on multiple threads
3. **Neural Network Evaluation**: Replace random simulations with learned evaluation
4. **Progressive Widening**: Limit child nodes initially, expand gradually
5. **RAVE (Rapid Action Value Estimation)**: Share statistics across similar positions

### State Copying

The current implementation uses `copy.deepcopy()` for state duplication. This is correct but potentially slow. For better performance:
- Implement a custom `copy()` method on `Grid`
- Use numpy arrays instead of nested lists
- Implement copy-on-write semantics

---

## Code Quality Notes

### Strengths
- Clean separation of concerns
- Well-documented game logic
- Comprehensive test coverage
- Proper error handling with exceptions
- Clear class hierarchies

### Potential Improvements

1. **Type Hints**: Add type annotations throughout
   ```python
   def add_piece(self, column: int, piece: int) -> bool:
   ```

2. **Constants**: Define magic numbers as constants
   ```python
   DEFAULT_ROWS = 6
   DEFAULT_COLUMNS = 7
   CONNECT_LENGTH = 4
   ```

3. **Enums**: Use enums for player pieces and results
   ```python
   from enum import Enum
   class Piece(Enum):
       EMPTY = 0
       PLAYER_ONE = 1
       PLAYER_TWO = 2
   ```

4. **Logging**: Add logging for debugging AI decisions
   ```python
   import logging
   logging.info(f"MCTS selected move {best_move} with {visits} visits")
   ```

5. **Configuration**: Move game parameters to config file
   ```python
   # config.py
   GRID_ROWS = 6
   GRID_COLUMNS = 7
   MCTS_ITERATIONS = 1000
   EXPLORATION_CONSTANT = 1.414
   ```

---

## Extending the Project

### Adding New Features

1. **Different Board Sizes**
   - Modify `Grid.__init__()` to accept custom dimensions
   - Adjust win detection for different grid sizes

2. **Adjustable Win Condition**
   - Change from 4-in-a-row to N-in-a-row
   - Pass `win_length` parameter to `Grid`

3. **Move History**
   - Add `history: List[int]` to `Grid`
   - Implement undo/redo functionality

4. **Save/Load Games**
   - Serialize grid state to JSON
   - Implement game replay feature

5. **GUI**
   - Use pygame or tkinter for graphical interface
   - Visualize MCTS tree exploration

6. **Network Play**
   - Add client-server architecture
   - Implement remote multiplayer

### Algorithm Enhancements

1. **AlphaZero-style MCTS**
   - Add neural network for position evaluation
   - Train through self-play

2. **Minimax with Alpha-Beta Pruning**
   - Alternative to MCTS for comparison
   - Useful for understanding different search strategies

3. **Opening Book**
   - Pre-computed best moves for early game
   - Skip MCTS for first few moves

---

## References

### MCTS Resources
- [Monte Carlo Tree Search - Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
- [A Survey of Monte Carlo Tree Search Methods](https://ieeexplore.ieee.org/document/6145622)
- [UCB1 Algorithm](https://en.wikipedia.org/wiki/Upper_confidence_bound)

### Connect 4 Game Theory
- [Connect Four is Solved](https://connect4.gamesolver.org/)
- First player can force a win with perfect play
- Center column is the strongest opening

### Python Best Practices
- [PEP 8 - Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)

---

## License

This project is provided as-is for educational purposes.

## Contributors

Developed as a demonstration of MCTS algorithms in game playing.
