import pytest
from grid import Grid
from player import BotPlayer

# --- Grid Tests ---
def test_add_piece_and_valid_moves():
    grid = Grid()
    # All columns should be valid at start
    assert grid.get_valid_moves() == list(range(grid.columns))
    # Add a piece to column 0
    assert grid.add_piece(0, 1) is True
    # Column 0 should still be valid (not full)
    assert 0 in grid.get_valid_moves()
    # Fill up column 0
    for _ in range(grid.rows - 1):
        grid.add_piece(0, 2)
    # Now column 0 should be full
    assert 0 not in grid.get_valid_moves()
    # Adding to a full column should raise
    with pytest.raises(ValueError):
        grid.add_piece(0, 1)
    # Invalid column
    with pytest.raises(ValueError):
        grid.add_piece(-1, 1)
    with pytest.raises(ValueError):
        grid.add_piece(grid.columns, 1)

def test_horizontal_win():
    grid = Grid()
    for col in range(4):
        grid.add_piece(col, 1)
    assert grid.is_winner(1)

def test_vertical_win():
    grid = Grid()
    for _ in range(4):
        grid.add_piece(0, 2)
    assert grid.is_winner(2)

def test_diagonal_win():
    grid = Grid()
    # Down-right diagonal for player 1
    for i in range(4):
        for _ in range(i):
            grid.add_piece(i, 2)
        grid.add_piece(i, 1)
    assert grid.is_winner(1)

def test_botplayer_move_is_valid():
    grid = Grid()
    bot = BotPlayer("AI", "red")
    move = bot.play(grid)
    assert move in grid.get_valid_moves()
    # Fill all but one column
    for col in range(grid.columns - 1):
        for _ in range(grid.rows):
            grid.add_piece(col, 1)
    move = bot.play(grid)
    assert move == grid.columns - 1 