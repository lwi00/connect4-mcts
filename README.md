# Connect 4 with MCTS AI

A Python implementation of Connect 4 featuring an AI opponent powered by Monte Carlo Tree Search (MCTS). This project demonstrates advanced game-playing algorithms, object-oriented design, and comprehensive software testing practices.

## Features

- **Classic Connect 4 gameplay** with a 6x7 grid
- **Multiple game modes**:
  - Human vs Human
  - Human vs AI
  - AI vs AI (watch two AIs battle!)
- **Intelligent MCTS AI** with configurable difficulty
- **Tactical awareness**: AI detects immediate wins and blocks opponent threats
- **UCB1 algorithm** for balanced exploration-exploitation
- **Object-oriented design** with clean separation of concerns
- **Comprehensive test suite** with 15+ test cases

## Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/connect4-mcts.git
   cd connect4-mcts
   ```

2. Install dependencies:
   ```bash
   pip install numpy pytest
   ```

### Running the Game

```bash
python main.py
```

### Game Controls

1. Choose your game mode:
   - **1**: Human vs Human
   - **2**: Human vs AI (test your skills!)
   - **3**: AI vs AI (watch the algorithms compete)

2. For human players, enter your name when prompted

3. Take turns placing pieces by entering a column number (0-6)

4. First player to get 4 pieces in a row wins!

**Win Conditions:**
- Horizontal: 4 in a row across
- Vertical: 4 in a row down
- Diagonal: 4 in a row diagonally (both directions)

## How the AI Works

The AI uses **Monte Carlo Tree Search (MCTS)**, a powerful algorithm that evaluates positions through random simulations. Here's how it works:

### MCTS Algorithm

1. **Selection**: Navigate the game tree using UCB1 to balance exploration and exploitation
2. **Expansion**: Create new nodes for unexplored moves
3. **Simulation**: Play random games from the new position
4. **Backpropagation**: Update statistics based on simulation results

### Key Features

- **UCB1 Formula**: `win_rate + c * sqrt(ln(parent_visits) / visits)`
  - Balances trying new moves (exploration) with playing known good moves (exploitation)
  - The constant `c = 1.414` (√2) controls this balance

- **Tactical Layer**: Before running MCTS, the AI checks for:
  - **Immediate wins**: If AI can win now, it does
  - **Immediate blocks**: If opponent can win next turn, AI blocks them
  - This prevents the AI from missing obvious tactical moves

- **Configurable Strength**:
  - More iterations = stronger AI but slower response
  - Default: 1000 iterations (~1 second per move)
  - Easy: 100-500 iterations
  - Hard: 5000+ iterations

## Project Structure

```
connect4-mcts/
├── main.py              # Entry point - launches the game
├── connect_four.py      # Game orchestration and flow control
├── grid.py              # Board representation and game rules
├── player.py            # Player classes (Human and Bot)
├── node.py              # MCTS tree node implementation
├── mcts.py              # Monte Carlo Tree Search algorithm
├── test_connect4.py     # Comprehensive test suite
├── README.md            # This file
└── DOCUMENTATION.md     # Detailed technical documentation
```

### File Descriptions

- **`main.py`**: Simple entry point that creates and launches the game
- **`connect_four.py`**: Main game class handling player setup and game loop
- **`grid.py`**: Core game logic including win detection and move validation
- **`player.py`**: Abstract `Player` class with `HumanPlayer` and `BotPlayer` implementations
- **`node.py`**: Tree node structure for MCTS with statistics tracking
- **`mcts.py`**: Complete MCTS implementation with UCB1 selection
- **`test_connect4.py`**: pytest test suite covering grid logic, MCTS, and AI behavior

## Testing

Run the test suite to verify everything works:

```bash
# Run all tests
pytest test_connect4.py

# Run with verbose output
pytest test_connect4.py -v

# Run specific test
pytest test_connect4.py::test_mcts_finds_immediate_win
```

### Test Coverage

- **Grid Tests**: Piece placement, win detection (horizontal, vertical, diagonal), draw conditions
- **MCTS Tests**: Valid move generation, winning move detection, blocking logic
- **Integration Tests**: Bot player behavior in various scenarios

## Requirements

- **Python 3.7+**
- **numpy**: For mathematical operations in MCTS
- **pytest**: For running the test suite (development only)

Install with:
```bash
pip install numpy pytest
```

## Advanced Usage

### Adjusting AI Difficulty

Edit `connect_four.py` to change AI strength:

```python
# Line 65 and 68-69
self._addPlayer("AI", 'yellow', is_bot=True, iterations=100)    # Easy
self._addPlayer("AI", 'yellow', is_bot=True, iterations=1000)   # Medium (default)
self._addPlayer("AI", 'yellow', is_bot=True, iterations=5000)   # Hard
```

### Customizing Board Size

Edit `grid.py`:

```python
# Edit default parameters in Grid.__init__() method (line 2)
def __init__(self, rows=6, columns=7):  # Change dimensions here
```

Note: Win detection assumes 4-in-a-row. For different win conditions, modify `is_winner()` method.

### Tuning MCTS Exploration

Edit `mcts.py`:

```python
# Line 7
def __init__(self, exploration_constant=1.414):  # Default: sqrt(2)
    # Lower values: More exploitation (greedy)
    # Higher values: More exploration (risky)
```

## Performance

### AI Response Times (approximate)

| Iterations | Response Time | Skill Level |
|-----------|---------------|-------------|
| 100       | ~0.1s        | Easy        |
| 500       | ~0.5s        | Medium-Easy |
| 1000      | ~1s          | Medium      |
| 2000      | ~2s          | Medium-Hard |
| 5000      | ~5s          | Hard        |
| 10000     | ~10s         | Very Hard   |

*Times vary based on CPU speed and position complexity*

### Memory Usage

- Typical: <10 MB
- Per iteration: ~200 bytes/node
- Memory released after each move

## Technical Documentation

For detailed technical information, see [DOCUMENTATION.md](DOCUMENTATION.md):

- Complete architecture overview
- Detailed API reference
- MCTS algorithm explanation
- Performance optimization tips
- Extension ideas and code quality notes

## Game Theory

**Connect 4 is a solved game**: With perfect play, the first player can always force a win. The center column (column 3) is the strongest opening move.

Our MCTS AI doesn't play perfectly (that would require massive computational resources), but it plays very well with sufficient iterations.

## Contributing

Contributions are welcome! Areas for improvement:

1. Add type hints throughout the codebase
2. Implement game save/load functionality
3. Create a GUI using pygame or tkinter
4. Add neural network evaluation (AlphaZero-style)
5. Implement parallel MCTS for faster searches
6. Add opening book for early-game moves

## Troubleshooting

**AI is too slow:**
- Reduce iterations in `connect_four.py` (lines 65, 68-69)
- Default 1000 iterations is reasonable for most systems

**Tests failing:**
- Ensure numpy is installed: `pip install numpy`
- Check Python version: `python --version` (requires 3.7+)
- Run with verbose output: `pytest test_connect4.py -v`

**Game not starting:**
- Verify you're in the correct directory
- Check that all .py files are present
- Try: `python3 main.py` instead of `python main.py`

## License

This project is provided as-is for educational purposes. Feel free to use, modify, and learn from the code.

## Acknowledgments

- MCTS algorithm based on the UCT variant by Kocsis & Szepesvári
- Connect 4 game rules and win detection logic
- Inspired by AlphaGo and AlphaZero's use of MCTS

## Learn More

- Read [DOCUMENTATION.md](DOCUMENTATION.md) for technical deep-dive
- Study the test cases to understand expected behavior
- Experiment with different MCTS parameters
- Try implementing your own evaluation function

---

**Enjoy the game! May the best algorithm win!**
