"""Tests for main entrypoint."""

import runpy
from unittest.mock import patch

import main


def test_main_calls_ui_run() -> None:
    """main() creates UI and calls run."""
    with patch("main.HanoiUI") as mock_ui:
        main.main()
    mock_ui.return_value.run.assert_called_once()


def test_module_entrypoint_calls_main() -> None:
    """Running module as __main__ triggers UI run."""
    with patch("ui.HanoiUI") as mock_ui:
        runpy.run_module("main", run_name="__main__")
    mock_ui.return_value.run.assert_called_once()
