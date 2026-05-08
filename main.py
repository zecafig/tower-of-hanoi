"""Main entry point for Tower of Hanoi game."""

from ui import HanoiUI


def main() -> None:
    """Run the Tower of Hanoi game."""
    ui = HanoiUI()
    ui.run()


if __name__ == "__main__":
    main()
