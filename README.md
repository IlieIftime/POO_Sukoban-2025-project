# Sokoban Game

A desktop Sokoban puzzle game built with Python and Pygame. The project
includes five levels, keyboard controls, sprites, level validation, and
optional background music.

## Requirements

- Python 3.11+
- Pygame 2.6.0

## Setup

From the project root on Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks script activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

The repository already contains a `.venv` directory when the environment has
been created. Do not commit virtual-environment files.

## Run

Music is disabled by default:

```powershell
python main.py
```

Enable the bundled music with:

```powershell
python main.py --music
```

Use `--no-music` to explicitly keep music disabled.

## Controls

- Arrow keys or `WASD`: move
- `R`: reset the current level
- `P`: pause or resume
- Close the window: exit

## Project layout

```text
main.py              Application entry point
GameEngine.py        Main game loop and rendering
level/               Level definitions and loader
classes/             Game objects and custom exceptions
collection/           Image loading utilities
images/              Game assets
lamusica.mp3         Optional background music
```
