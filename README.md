# Connect 4 with MCTS AI

A Python implementation of Connect 4 with Monte Carlo Tree Search (MCTS) AI.

## Features

- **Classic Connect 4 gameplay** with a 6x7 grid
- **Multiple game modes**:
  - Human vs Human
  - Human vs AI
  - AI vs AI
- **MCTS AI** that improves with more iterations
- **Object-oriented design** with clean separation of concerns
- **Comprehensive test suite** using pytest

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Choose your game mode:
   - **1**: Human vs Human
   - **2**: Human vs AI
   - **3**: AI vs AI

3. For human players, enter your name when prompted

4. Take turns placing pieces by choosing a column (0-6)

5. First player to get 4 pieces in a row (horizontal, vertical, or diagonal) wins!

## AI Features

The MCTS AI uses Monte Carlo Tree Search to find the best moves:

- **Exploration vs Exploitation**: Balances trying new moves with focusing on promising ones
- **Configurable strength**: Adjust iterations for different AI difficulty levels
- **No evaluation function needed**: Uses random playouts to estimate position strength

## Project Structure

- `main.py` - Entry point
- `connect_four.py` - Main game logic
- `grid.py` - Board representation and game rules
- `player.py` - Player classes (Human and AI)
- `node.py` - MCTS tree node implementation
- `mcts.py` - Monte Carlo Tree Search algorithm
- `test_connect4.py` - Test suite

## Running Tests

```bash
pytest test_connect4.py
```

## Requirements

- Python 3.7+
- pytest (for testing)
- numpy (for MCTS calculations)
