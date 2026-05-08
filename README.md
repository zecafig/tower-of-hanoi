# Tower of Hanoi

![CI](https://github.com/zecafig/tower-of-hanoi/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

Tower of Hanoi game built with pygame, developed as an AI coding test in GitHub Copilot.

## AI Test Metadata
- Tooling: GitHub Copilot (VS Code)
- LLM: Claude Haiku 4.5
- Prompt token usage: Not exposed by this VS Code Copilot environment
- Completion token usage: Not exposed by this VS Code Copilot environment

## Project Summary
- Traditional Tower of Hanoi gameplay with 3 towers and variable piece count
- Piece count prompt before game starts
- Keyboard controls:
  - N: start a new game and enter a new piece count
  - R: reset current game
  - Q: quit game
- Visual selection marker for currently selected tower
- Material-inspired visual palette

## Tech Stack
- Python
- pygame (via pygame-ce package)
- pytest
- pytest-cov
- ruff

## Local Run
```bash
source .venv/bin/activate
python ui.py
```

## Local Validation
```bash
source .venv/bin/activate
python -m ruff check .
python -m pytest --cov=. --cov-report=term-missing --cov-fail-under=100
```

## Repository Notes
- CI runs on every pull request
- Coverage gate is enforced at 100%
