"""Tower of Hanoi UI using pygame with Material Design."""

import pygame

from game import HanoiGame

# Material Design colors
MD_PRIMARY = (63, 81, 181)
MD_SELECTED = (255, 152, 0)
MD_LIGHT_BG = (245, 245, 245)
MD_TEXT = (33, 33, 33)
MD_TEXT_SECONDARY = (117, 117, 117)
MD_SUCCESS = (76, 175, 80)


class HanoiUI:
    """Pygame UI for Tower of Hanoi game using Material Design."""

    def __init__(self):
        """Initialize the UI."""
        pygame.init()
        self.width = 1000
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower of Hanoi")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 16)
        self.clock = pygame.time.Clock()
        self.game = None
        self.selected_tower = None
        self.running = True

    def get_number_of_pieces(self) -> int:
        """Prompt user to enter number of pieces.
        
        Returns:
            Number of pieces chosen by user.
        """
        input_text = ""

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit() and int(input_text) > 0:
                            return int(input_text)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        if len(input_text) < 2:
                            input_text += event.unicode
            
            self.screen.fill(MD_LIGHT_BG)
            self._draw_input_screen(input_text)
            pygame.display.flip()
            self.clock.tick(60)
        
        return 0

    def _draw_input_screen(self, input_text: str) -> None:
        """Draw the input screen for number of pieces.
        
        Args:
            input_text: Current input text.
        """
        # Title
        title = self.font_large.render("Tower of Hanoi", True, MD_PRIMARY)
        self.screen.blit(
            title,
            (self.width // 2 - title.get_width() // 2, 100),
        )
        
        # Instruction
        instruction = self.font_medium.render(
            "Enter number of pieces:",
            True,
            MD_TEXT,
        )
        self.screen.blit(
            instruction,
            (self.width // 2 - instruction.get_width() // 2, 250),
        )
        
        # Input box
        input_rect = pygame.Rect(
            self.width // 2 - 100,
            350,
            200,
            60,
        )
        pygame.draw.rect(self.screen, MD_PRIMARY, input_rect, 2)
        
        # Input text
        text_surface = self.font_medium.render(
            input_text or "0",
            True,
            MD_PRIMARY,
        )
        self.screen.blit(
            text_surface,
            (
                input_rect.x + 10,
                input_rect.y + 15,
            ),
        )
        
        # Hint
        hint = self.font_small.render(
            "Press ENTER to start",
            True,
            MD_TEXT_SECONDARY,
        )
        self.screen.blit(
            hint,
            (self.width // 2 - hint.get_width() // 2, 480),
        )

    def _get_tower_positions(self) -> list:
        """Get the x positions of the three towers.
        
        Returns:
            List of x positions for towers.
        """
        return [
            self.width // 4,
            self.width // 2,
            3 * self.width // 4,
        ]

    def _draw_towers(self) -> None:
        """Draw the three towers."""
        tower_x_positions = self._get_tower_positions()
        base_y = self.height - 100
        
        for tower_idx, tower_x in enumerate(tower_x_positions):
            # Draw base
            pygame.draw.rect(
                self.screen,
                MD_TEXT,
                (tower_x - 60, base_y, 120, 10),
            )
            
            # Draw pole
            pygame.draw.line(
                self.screen,
                MD_TEXT,
                (tower_x, base_y - 200),
                (tower_x, base_y),
                3,
            )
            
            # Draw pieces
            pieces = self.game.towers[tower_idx]
            for piece_idx, piece_size in enumerate(pieces):
                piece_width = 20 + piece_size * 15
                piece_height = 20
                piece_x = tower_x - piece_width // 2
                piece_y = base_y - 30 - (piece_idx + 1) * 30
                
                # Color based on piece
                color = self._get_piece_color(piece_size)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (piece_x, piece_y, piece_width, piece_height),
                )
                pygame.draw.rect(
                    self.screen,
                    MD_TEXT,
                    (piece_x, piece_y, piece_width, piece_height),
                    2,
                )

            if tower_idx == self.selected_tower:
                self._draw_selected_tower_marker(tower_x, base_y)

    def _draw_selected_tower_marker(self, tower_x: int, base_y: int) -> None:
        """Draw a clear visual marker for the selected tower."""
        pygame.draw.circle(
            self.screen,
            MD_SELECTED,
            (tower_x, base_y + 26),
            13,
            3,
        )
        pygame.draw.polygon(
            self.screen,
            MD_SELECTED,
            [
                (tower_x, base_y - 220),
                (tower_x - 10, base_y - 202),
                (tower_x + 10, base_y - 202),
            ],
        )

    def _get_piece_color(self, piece_size: int) -> tuple:
        """Get color for a piece based on its size.
        
        Args:
            piece_size: Size of the piece (1 to num_pieces).
            
        Returns:
            RGB color tuple.
        """
        colors = [
            (244, 67, 54),
            (233, 30, 99),
            (156, 39, 176),
            (103, 58, 183),
            (63, 81, 181),
            (33, 150, 243),
            (3, 169, 244),
        ]
        return colors[min(piece_size - 1, len(colors) - 1)]

    def _draw_hud(self) -> None:
        """Draw heads-up display (moves, optimal moves, controls)."""
        # Move count
        moves_text = self.font_medium.render(
            f"Moves: {self.game.move_count}",
            True,
            MD_TEXT,
        )
        self.screen.blit(moves_text, (20, 20))
        
        # Optimal moves
        optimal_text = self.font_small.render(
            f"Optimal: {self.game.get_optimal_moves()}",
            True,
            MD_TEXT_SECONDARY,
        )
        self.screen.blit(optimal_text, (20, 60))
        
        # Instructions
        inst_y = self.height - 30
        instructions = self.font_tiny.render(
            "Click tower to select source, click again to select destination | N: New Game | R: Reset | Q: Quit",
            True,
            MD_TEXT_SECONDARY,
        )
        self.screen.blit(instructions, (20, inst_y))

    def _draw_win_screen(self) -> None:
        """Draw the win screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Win message
        win_text = self.font_large.render("You Win!", True, MD_SUCCESS)
        self.screen.blit(
            win_text,
            (self.width // 2 - win_text.get_width() // 2, 150),
        )
        
        # Stats
        stats_text = self.font_medium.render(
            f"Moves: {self.game.move_count} / Optimal: {self.game.get_optimal_moves()}",
            True,
            MD_SUCCESS,
        )
        self.screen.blit(
            stats_text,
            (self.width // 2 - stats_text.get_width() // 2, 300),
        )
        
        # Instructions
        inst_text = self.font_small.render(
            "Press N for new game, R to reset, or Q to quit",
            True,
            (255, 255, 255),
        )
        self.screen.blit(
            inst_text,
            (self.width // 2 - inst_text.get_width() // 2, 400),
        )

    def _get_tower_at_position(self, x: int, y: int) -> int | None:
        """Get tower index at given screen position.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            
        Returns:
            Tower index (0, 1, 2) or None if not on a tower.
        """
        tower_x_positions = self._get_tower_positions()
        base_y = self.height - 100
        
        if not (base_y - 200 <= y <= base_y):
            return None
        
        for tower_idx, tower_x in enumerate(tower_x_positions):
            if abs(x - tower_x) < 80:
                return tower_idx
        
        return None

    def _handle_click(self, x: int, y: int) -> None:
        """Handle mouse click.
        
        Args:
            x: X coordinate of click.
            y: Y coordinate of click.
        """
        tower_idx = self._get_tower_at_position(x, y)
        
        if tower_idx is None:
            return
        
        if self.selected_tower is None:
            # Select source tower
            if self.game.towers[tower_idx]:
                self.selected_tower = tower_idx
        else:
            # Try to move to destination tower
            if self.game.move_piece(self.selected_tower, tower_idx):
                self.selected_tower = None
            elif self.selected_tower == tower_idx:
                # Deselect
                self.selected_tower = None
            else:
                # Invalid move, try to select new source
                if self.game.towers[tower_idx]:
                    self.selected_tower = tower_idx

    def run(self) -> None:
        """Run the game loop."""
        num_pieces = self.get_number_of_pieces()
        
        if num_pieces == 0:
            pygame.quit()
            return
        
        self.game = HanoiGame(num_pieces)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_n:
                        new_piece_count = self.get_number_of_pieces()
                        if new_piece_count == 0:
                            self.running = False
                        else:
                            self.game = HanoiGame(new_piece_count)
                            self.selected_tower = None
                    elif event.key == pygame.K_r:
                        self.game.reset()
                        self.selected_tower = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game.game_over:
                        self._handle_click(event.pos[0], event.pos[1])
            
            self.screen.fill(MD_LIGHT_BG)
            self._draw_towers()
            self._draw_hud()
            
            if self.game.game_over:
                self._draw_win_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()


if __name__ == "__main__":
    ui = HanoiUI()
    ui.run()
