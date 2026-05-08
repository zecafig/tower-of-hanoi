"""Tests for Tower of Hanoi game logic."""

import pytest

from game import HanoiGame


class TestHanoiGameInit:
    """Tests for HanoiGame initialization."""

    def test_init_with_valid_pieces(self):
        """Test initialization with valid number of pieces."""
        game = HanoiGame(3)
        assert game.num_pieces == 3
        assert len(game.towers) == 3
        assert game.towers[0] == [3, 2, 1]
        assert game.towers[1] == []
        assert game.towers[2] == []
        assert game.move_count == 0
        assert game.game_over is False

    def test_init_with_one_piece(self):
        """Test initialization with one piece."""
        game = HanoiGame(1)
        assert game.num_pieces == 1
        assert game.towers[0] == [1]

    def test_init_with_many_pieces(self):
        """Test initialization with many pieces."""
        game = HanoiGame(10)
        assert game.num_pieces == 10
        assert len(game.towers[0]) == 10

    def test_init_with_zero_pieces_raises_error(self):
        """Test that zero pieces raises ValueError."""
        with pytest.raises(ValueError):
            HanoiGame(0)

    def test_init_with_negative_pieces_raises_error(self):
        """Test that negative pieces raises ValueError."""
        with pytest.raises(ValueError):
            HanoiGame(-1)

    def test_init_with_non_integer_raises_error(self):
        """Test that non-integer pieces raises ValueError."""
        with pytest.raises(ValueError):
            HanoiGame(3.5)


class TestHanoiGameValidMove:
    """Tests for move validation."""

    def test_valid_move_to_empty_tower(self):
        """Test valid move to an empty tower."""
        game = HanoiGame(3)
        assert game.is_valid_move(0, 1) is True

    def test_invalid_move_same_tower(self):
        """Test that moving to the same tower is invalid."""
        game = HanoiGame(3)
        assert game.is_valid_move(0, 0) is False

    def test_invalid_move_from_empty_tower(self):
        """Test that moving from empty tower is invalid."""
        game = HanoiGame(3)
        assert game.is_valid_move(1, 0) is False

    def test_valid_move_smaller_to_larger(self):
        """Test valid move of smaller piece to larger piece."""
        game = HanoiGame(3)
        game.move_piece(0, 1)
        assert game.is_valid_move(1, 2) is True

    def test_invalid_move_larger_to_smaller(self):
        """Test invalid move of larger piece to smaller piece."""
        game = HanoiGame(3)
        game.move_piece(0, 1)
        game.move_piece(0, 2)
        assert game.is_valid_move(2, 1) is False

    def test_invalid_tower_index(self):
        """Test invalid tower indices."""
        game = HanoiGame(3)
        assert game.is_valid_move(0, 3) is False
        assert game.is_valid_move(-1, 1) is False
        assert game.is_valid_move(0, -1) is False


class TestHanoiGameMove:
    """Tests for piece movement."""

    def test_successful_move(self):
        """Test successful piece movement."""
        game = HanoiGame(3)
        assert game.move_piece(0, 1) is True
        assert game.towers[0] == [3, 2]
        assert game.towers[1] == [1]
        assert game.move_count == 1

    def test_multiple_moves(self):
        """Test multiple consecutive moves."""
        game = HanoiGame(3)
        assert game.move_piece(0, 1) is True
        assert game.move_piece(0, 2) is True
        assert game.move_piece(1, 2) is True
        assert game.towers[0] == [3]
        assert game.towers[1] == []
        assert game.towers[2] == [2, 1]
        assert game.move_count == 3

    def test_invalid_move_returns_false(self):
        """Test that invalid move returns False and doesn't change state."""
        game = HanoiGame(3)
        game.move_piece(0, 1)
        game.move_piece(0, 2)
        initial_state = game.get_state()
        assert game.move_piece(2, 1) is False
        assert game.get_state() == initial_state
        assert game.move_count == 2

    def test_move_count_increments(self):
        """Test that move count increments correctly."""
        game = HanoiGame(2)
        assert game.move_count == 0
        game.move_piece(0, 1)
        assert game.move_count == 1
        game.move_piece(0, 2)
        assert game.move_count == 2


class TestHanoiGameWin:
    """Tests for win condition."""

    def test_win_condition_one_piece(self):
        """Test win condition with one piece."""
        game = HanoiGame(1)
        assert game.game_over is False
        game.move_piece(0, 2)
        assert game.game_over is True

    def test_win_condition_two_pieces(self):
        """Test win condition with two pieces."""
        game = HanoiGame(2)
        assert game.game_over is False
        game.move_piece(0, 1)
        game.move_piece(0, 2)
        game.move_piece(1, 2)
        assert game.game_over is True

    def test_game_not_over_before_winning(self):
        """Test that game is not over until final move."""
        game = HanoiGame(2)
        game.move_piece(0, 1)
        assert game.game_over is False
        game.move_piece(0, 2)
        assert game.game_over is False
        game.move_piece(1, 2)
        assert game.game_over is True


class TestHanoiGameState:
    """Tests for game state retrieval."""

    def test_get_state_initial(self):
        """Test getting initial game state."""
        game = HanoiGame(3)
        state = game.get_state()
        assert state["num_pieces"] == 3
        assert state["move_count"] == 0
        assert state["game_over"] is False
        assert state["towers"] == [[3, 2, 1], [], []]

    def test_get_state_after_moves(self):
        """Test getting game state after moves."""
        game = HanoiGame(3)
        game.move_piece(0, 1)
        game.move_piece(0, 2)
        state = game.get_state()
        assert state["move_count"] == 2
        assert state["towers"] == [[3], [1], [2]]

    def test_get_state_returns_copy(self):
        """Test that get_state returns a copy, not a reference."""
        game = HanoiGame(3)
        state1 = game.get_state()
        state1["towers"][0].pop()
        state2 = game.get_state()
        assert state2["towers"] == [[3, 2, 1], [], []]


class TestHanoiGameReset:
    """Tests for game reset."""

    def test_reset_to_initial_state(self):
        """Test resetting game to initial state."""
        game = HanoiGame(3)
        game.move_piece(0, 1)
        game.move_piece(0, 2)
        assert game.move_count == 2
        game.reset()
        assert game.move_count == 0
        assert game.game_over is False
        assert game.towers == [[3, 2, 1], [], []]

    def test_reset_after_win(self):
        """Test resetting game after winning."""
        game = HanoiGame(1)
        game.move_piece(0, 2)
        assert game.game_over is True
        game.reset()
        assert game.game_over is False
        assert game.move_count == 0


class TestHanoiGameOptimalMoves:
    """Tests for optimal moves calculation."""

    def test_optimal_moves_one_piece(self):
        """Test optimal moves for one piece (2^1 - 1 = 1)."""
        game = HanoiGame(1)
        assert game.get_optimal_moves() == 1

    def test_optimal_moves_two_pieces(self):
        """Test optimal moves for two pieces (2^2 - 1 = 3)."""
        game = HanoiGame(2)
        assert game.get_optimal_moves() == 3

    def test_optimal_moves_three_pieces(self):
        """Test optimal moves for three pieces (2^3 - 1 = 7)."""
        game = HanoiGame(3)
        assert game.get_optimal_moves() == 7

    def test_optimal_moves_ten_pieces(self):
        """Test optimal moves for ten pieces (2^10 - 1 = 1023)."""
        game = HanoiGame(10)
        assert game.get_optimal_moves() == 1023
