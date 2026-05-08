"""Tests for Tower of Hanoi UI."""

import runpy
from unittest.mock import MagicMock, patch

import pygame

from game import HanoiGame
from ui import HanoiUI


def _build_ui() -> HanoiUI:
    """Create a UI instance with pygame display/font mocked for tests."""
    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode", return_value=pygame.Surface((1000, 700))),
        patch("pygame.time.Clock", return_value=MagicMock()),
        patch("pygame.font.Font") as mock_font,
    ):
        font = MagicMock()
        font.render.return_value = pygame.Surface((140, 30))
        mock_font.return_value = font
        return HanoiUI()


def test_init_defaults() -> None:
    """UI starts with expected defaults."""
    ui = _build_ui()
    assert ui.width == 1000
    assert ui.height == 700
    assert ui.game is None
    assert ui.selected_tower is None
    assert ui.running is True


def test_get_number_of_pieces_valid_input() -> None:
    """Input loop returns a positive integer on Enter."""
    ui = _build_ui()
    events = [
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_3, unicode="3")],
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN, unicode="")],
    ]
    with patch("pygame.event.get", side_effect=events), patch("pygame.display.flip"):
        assert ui.get_number_of_pieces() == 3


def test_get_number_of_pieces_limits_to_two_digits() -> None:
    """Only two numeric digits are accepted in the input box."""
    ui = _build_ui()
    events = [
        [
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_1, unicode="1"),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_2, unicode="2"),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_3, unicode="3"),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN, unicode=""),
        ],
    ]
    with patch("pygame.event.get", side_effect=events), patch("pygame.display.flip"):
        assert ui.get_number_of_pieces() == 12


def test_get_number_of_pieces_backspace_path() -> None:
    """Backspace removes the last typed digit before submitting."""
    ui = _build_ui()
    events = [
        [
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_4, unicode="4"),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode=""),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_5, unicode="5"),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN, unicode=""),
        ],
    ]
    with patch("pygame.event.get", side_effect=events), patch("pygame.display.flip"):
        assert ui.get_number_of_pieces() == 5


def test_get_number_of_pieces_quit_event() -> None:
    """Quit event exits input loop and returns zero."""
    ui = _build_ui()
    events = [[MagicMock(type=pygame.QUIT)]]
    with patch("pygame.event.get", side_effect=events), patch("pygame.display.flip"):
        assert ui.get_number_of_pieces() == 0
        assert ui.running is False


def test_get_number_of_pieces_when_not_running() -> None:
    """If UI is already stopped, input prompt returns zero immediately."""
    ui = _build_ui()
    ui.running = False
    assert ui.get_number_of_pieces() == 0


def test_draw_input_screen() -> None:
    """Input screen can be rendered without error."""
    ui = _build_ui()
    with patch("pygame.draw.rect") as draw_rect:
        ui._draw_input_screen("3")
    draw_rect.assert_called()


def test_tower_positions() -> None:
    """Tower X positions are equally spaced."""
    ui = _build_ui()
    assert ui._get_tower_positions() == [ui.width // 4, ui.width // 2, 3 * ui.width // 4]


def test_draw_towers() -> None:
    """Tower and piece drawing calls are issued."""
    ui = _build_ui()
    ui.game = HanoiGame(3)
    with patch("pygame.draw.rect") as draw_rect, patch("pygame.draw.line") as draw_line:
        ui._draw_towers()
    assert draw_line.call_count == 3
    assert draw_rect.call_count >= 3


def test_draw_towers_shows_selected_marker() -> None:
    """Selected tower gets a visual marker for clearer UX."""
    ui = _build_ui()
    ui.game = HanoiGame(3)
    ui.selected_tower = 1
    with patch("pygame.draw.circle") as draw_circle, patch("pygame.draw.polygon") as draw_polygon:
        ui._draw_towers()
    draw_circle.assert_called_once()
    draw_polygon.assert_called_once()


def test_piece_color_bounds() -> None:
    """Piece color mapping handles valid and high indexes."""
    ui = _build_ui()
    assert ui._get_piece_color(1) == (244, 67, 54)
    assert ui._get_piece_color(7) == (3, 169, 244)
    assert ui._get_piece_color(12) == (3, 169, 244)


def test_draw_hud() -> None:
    """HUD rendering works for active game."""
    ui = _build_ui()
    ui.game = HanoiGame(3)
    ui._draw_hud()


def test_draw_win_screen() -> None:
    """Win overlay rendering works."""
    ui = _build_ui()
    ui.game = HanoiGame(1)
    ui.game.move_piece(0, 2)
    ui._draw_win_screen()


def test_get_tower_at_position() -> None:
    """Tower hit detection returns correct indices and None outside area."""
    ui = _build_ui()
    base_y = ui.height - 100
    assert ui._get_tower_at_position(ui.width // 4, base_y - 50) == 0
    assert ui._get_tower_at_position(ui.width // 2, base_y - 50) == 1
    assert ui._get_tower_at_position(3 * ui.width // 4, base_y - 50) == 2
    assert ui._get_tower_at_position(0, 0) is None
    assert ui._get_tower_at_position(ui.width // 4, base_y + 10) is None
    assert ui._get_tower_at_position(ui.width // 4 + 90, base_y - 50) is None


def test_handle_click_paths() -> None:
    """Click handling covers select, move, deselect, and invalid move branches."""
    ui = _build_ui()
    ui.game = HanoiGame(3)
    base_y = ui.height - 100
    tower_0 = ui.width // 4
    tower_1 = ui.width // 2

    ui._handle_click(0, 0)
    assert ui.selected_tower is None

    ui._handle_click(tower_0, base_y - 50)
    assert ui.selected_tower == 0

    ui._handle_click(tower_1, base_y - 50)
    assert ui.selected_tower is None

    ui._handle_click(tower_1, base_y - 50)
    assert ui.selected_tower == 1
    ui._handle_click(tower_1, base_y - 50)
    assert ui.selected_tower is None

    ui.game.move_piece(0, 2)
    ui.selected_tower = 2
    ui._handle_click(tower_1, base_y - 50)
    assert ui.selected_tower == 1

    ui = _build_ui()
    ui.game = HanoiGame(3)
    ui._handle_click(tower_1, base_y - 50)
    assert ui.selected_tower is None


def test_init_autoplay_defaults() -> None:
    """Autoplay state initialises empty with correct delay."""
    ui = _build_ui()
    assert ui.autoplay_moves == []
    assert ui.autoplay_timer == 0
    assert ui.autoplay_delay == 500


def test_tick_autoplay_does_nothing_when_empty() -> None:
    """_tick_autoplay is a no-op when there are no pending moves."""
    ui = _build_ui()
    ui.game = HanoiGame(3)
    ui._tick_autoplay()
    assert ui.game.move_count == 0


def test_tick_autoplay_does_nothing_when_game_over() -> None:
    """_tick_autoplay stops when the game is already won."""
    ui = _build_ui()
    ui.game = HanoiGame(1)
    ui.game.move_piece(0, 2)
    ui.autoplay_moves = [(0, 2)]
    ui._tick_autoplay()
    assert ui.game.move_count == 1  # No extra move applied


def test_tick_autoplay_executes_move_after_delay() -> None:
    """A move is executed once the delay threshold is exceeded."""
    ui = _build_ui()
    ui.game = HanoiGame(1)
    ui.autoplay_moves = [(0, 2)]
    ui.autoplay_timer = 500
    ui.clock.get_time = MagicMock(return_value=0)
    ui._tick_autoplay()
    assert ui.game.move_count == 1
    assert ui.autoplay_moves == []
    assert ui.autoplay_timer == 0


def test_tick_autoplay_does_not_move_before_delay() -> None:
    """No move is made if the timer has not yet reached the delay."""
    ui = _build_ui()
    ui.game = HanoiGame(1)
    ui.autoplay_moves = [(0, 2)]
    ui.autoplay_timer = 0
    ui.clock.get_time = MagicMock(return_value=100)
    ui._tick_autoplay()
    assert ui.game.move_count == 0


def test_draw_hud_shows_autoplay_indicator() -> None:
    """HUD renders an autoplay indicator when moves are queued."""
    ui = _build_ui()
    ui.game = HanoiGame(3)
    ui.autoplay_moves = [(0, 2), (0, 1)]
    ui._draw_hud()


def test_run_a_key_starts_autoplay() -> None:
    """Pressing A resets the game and queues the optimal move sequence."""
    ui = _build_ui()
    events = [
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_a)],
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_q)],
    ]
    with (
        patch.object(ui, "get_number_of_pieces", return_value=2),
        patch("pygame.event.get", side_effect=events),
        patch.object(ui, "_tick_autoplay"),
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch.object(ui, "_draw_win_screen"),
        patch("pygame.display.flip"),
        patch("pygame.quit"),
    ):
        ui.run()
    assert ui.game.num_pieces == 2
    assert ui.selected_tower is None


def test_run_click_blocked_during_autoplay() -> None:
    """Mouse clicks are ignored while autoplay is in progress."""
    ui = _build_ui()
    events = [
        [MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(250, 550))],
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_q)],
    ]
    with (
        patch.object(ui, "get_number_of_pieces", return_value=2),
        patch("pygame.event.get", side_effect=events),
        patch.object(ui, "_handle_click") as mock_click,
        patch.object(ui, "_tick_autoplay"),
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch.object(ui, "_draw_win_screen"),
        patch("pygame.display.flip"),
        patch("pygame.quit"),
    ):
        ui.autoplay_moves = [(0, 2)]
        ui.run()
    mock_click.assert_not_called()


def test_run_exits_when_piece_count_is_zero() -> None:
    """Run exits early when user cancels at input prompt."""
    ui = _build_ui()
    with patch.object(ui, "get_number_of_pieces", return_value=0), patch("pygame.quit") as quit_mock:
        ui.run()
    quit_mock.assert_called_once()


def test_run_processes_key_and_mouse_events() -> None:
    """Run loop handles reset, click, and quit branches."""
    ui = _build_ui()
    events = [
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_r)],
        [MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(123, 456))],
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_q)],
    ]

    with (
        patch.object(ui, "get_number_of_pieces", return_value=1),
        patch("pygame.event.get", side_effect=events),
        patch.object(ui, "_handle_click") as handle_click,
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch.object(ui, "_draw_win_screen"),
        patch("pygame.display.flip"),
        patch("pygame.quit") as quit_mock,
    ):
        ui.run()

    handle_click.assert_called_once_with(123, 456)
    quit_mock.assert_called_once()


def test_run_starts_new_game_with_n_key() -> None:
    """Pressing N prompts for a new piece count and starts a new game."""
    ui = _build_ui()
    events = [
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_n)],
        [MagicMock(type=pygame.KEYDOWN, key=pygame.K_q)],
    ]

    with (
        patch.object(ui, "get_number_of_pieces", side_effect=[1, 4]),
        patch("pygame.event.get", side_effect=events),
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch.object(ui, "_draw_win_screen"),
        patch("pygame.display.flip"),
        patch("pygame.quit") as quit_mock,
    ):
        ui.run()

    assert ui.game.num_pieces == 4
    assert ui.selected_tower is None
    quit_mock.assert_called_once()


def test_run_n_key_cancel_stops_game() -> None:
    """If N prompt is canceled, the game exits cleanly."""
    ui = _build_ui()
    events = [[MagicMock(type=pygame.KEYDOWN, key=pygame.K_n)]]

    with (
        patch.object(ui, "get_number_of_pieces", side_effect=[1, 0]),
        patch("pygame.event.get", side_effect=events),
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch.object(ui, "_draw_win_screen"),
        patch("pygame.display.flip"),
        patch("pygame.quit") as quit_mock,
    ):
        ui.run()

    assert ui.running is False
    quit_mock.assert_called_once()


def test_run_draws_win_overlay_when_game_is_over() -> None:
    """Run loop draws win screen when game_over is true."""
    ui = _build_ui()
    fake_game = MagicMock()
    fake_game.game_over = True

    with (
        patch.object(ui, "get_number_of_pieces", return_value=1),
        patch("ui.HanoiGame", return_value=fake_game),
        patch("pygame.event.get", side_effect=[[MagicMock(type=pygame.KEYDOWN, key=pygame.K_q)]]),
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch.object(ui, "_draw_win_screen") as draw_win,
        patch("pygame.display.flip"),
        patch("pygame.quit"),
    ):
        ui.run()

    draw_win.assert_called_once()


def test_run_handles_quit_event() -> None:
    """Run loop exits when a QUIT event is received."""
    ui = _build_ui()
    with (
        patch.object(ui, "get_number_of_pieces", return_value=1),
        patch("pygame.event.get", side_effect=[[MagicMock(type=pygame.QUIT)]]),
        patch.object(ui, "_draw_towers"),
        patch.object(ui, "_draw_hud"),
        patch("pygame.display.flip"),
        patch("pygame.quit") as quit_mock,
    ):
        ui.run()
    quit_mock.assert_called_once()


def test_ui_module_entrypoint_calls_run() -> None:
    """Running ui module as __main__ executes HanoiUI.run()."""
    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode", return_value=pygame.Surface((1000, 700))),
        patch("pygame.time.Clock", return_value=MagicMock()),
        patch("pygame.font.Font") as mock_font,
        patch("pygame.event.get", return_value=[MagicMock(type=pygame.QUIT)]),
        patch("pygame.display.flip"),
        patch("pygame.quit") as quit_mock,
    ):
        font = MagicMock()
        font.render.return_value = pygame.Surface((140, 30))
        mock_font.return_value = font
        runpy.run_module("ui", run_name="__main__")
    quit_mock.assert_called_once()
