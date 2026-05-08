"""Tower of Hanoi game logic."""


class HanoiGame:
    """Manages the state and logic of Tower of Hanoi game."""

    def __init__(self, num_pieces: int):
        """Initialize the game with a given number of pieces.
        
        Args:
            num_pieces: Number of pieces to use in the game (must be > 0).
            
        Raises:
            ValueError: If num_pieces is not positive.
        """
        if not isinstance(num_pieces, int) or num_pieces <= 0:
            raise ValueError("Number of pieces must be a positive integer")
        
        self.num_pieces = num_pieces
        # Initialize towers: tower 0 starts with all pieces
        self.towers = [list(range(num_pieces, 0, -1)), [], []]
        self.move_count = 0
        self.game_over = False

    def is_valid_move(self, source: int, destination: int) -> bool:
        """Check if a move from source to destination tower is valid.
        
        Args:
            source: Index of source tower (0, 1, or 2).
            destination: Index of destination tower (0, 1, or 2).
            
        Returns:
            True if the move is valid, False otherwise.
        """
        if not (0 <= source <= 2 and 0 <= destination <= 2):
            return False
        if source == destination:
            return False
        if not self.towers[source]:
            return False
        if not self.towers[destination]:
            return True
        return self.towers[source][-1] < self.towers[destination][-1]

    def move_piece(self, source: int, destination: int) -> bool:
        """Move a piece from source tower to destination tower.
        
        Args:
            source: Index of source tower (0, 1, or 2).
            destination: Index of destination tower (0, 1, or 2).
            
        Returns:
            True if move was successful, False otherwise.
        """
        if not self.is_valid_move(source, destination):
            return False
        
        piece = self.towers[source].pop()
        self.towers[destination].append(piece)
        self.move_count += 1
        
        if self._check_win():
            self.game_over = True
        
        return True

    def _check_win(self) -> bool:
        """Check if the game is won (all pieces on tower 2).
        
        Returns:
            True if game is won, False otherwise.
        """
        return len(self.towers[2]) == self.num_pieces

    def get_state(self) -> dict:
        """Get current game state.
        
        Returns:
            Dictionary containing game state.
        """
        return {
            "towers": [tower[:] for tower in self.towers],
            "move_count": self.move_count,
            "game_over": self.game_over,
            "num_pieces": self.num_pieces,
        }

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.towers = [list(range(self.num_pieces, 0, -1)), [], []]
        self.move_count = 0
        self.game_over = False

    def get_optimal_moves(self) -> int:
        """Calculate optimal number of moves to solve the puzzle.
        
        Returns:
            Optimal number of moves (2^n - 1).
        """
        return (2 ** self.num_pieces) - 1

    def solve(self) -> list[tuple[int, int]]:
        """Return the optimal sequence of moves to solve the puzzle.

        Returns:
            List of (source, destination) index pairs.
        """
        moves: list[tuple[int, int]] = []

        def _hanoi(n: int, source: int, destination: int, auxiliary: int) -> None:
            if n == 1:
                moves.append((source, destination))
                return
            _hanoi(n - 1, source, auxiliary, destination)
            moves.append((source, destination))
            _hanoi(n - 1, auxiliary, destination, source)

        _hanoi(self.num_pieces, 0, 2, 1)
        return moves
