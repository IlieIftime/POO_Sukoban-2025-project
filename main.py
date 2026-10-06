import argparse

import pygame
from GameEngine import GameEngine
from classes.excessoes import LevelFileError
from level.levelloader import LevelLoader


def parse_args():
    """Parse command-line options for the game."""
    parser = argparse.ArgumentParser(description="Run the Sokoban game.")
    music_group = parser.add_mutually_exclusive_group()
    music_group.add_argument(
        "--music",
        dest="music_enabled",
        action="store_true",
        help="enable background music (disabled by default)",
    )
    music_group.add_argument(
        "--no-music",
        dest="music_enabled",
        action="store_false",
        help="keep background music disabled",
    )
    parser.set_defaults(music_enabled=False)
    return parser.parse_args()


def main():
    """Initialize and run the game."""
    args = parse_args()
    try:
        pygame.init()

        screen_width, screen_height = 1000, 1000
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Sokoban Game")

        level_files = [
            "level/level1.txt",
            "level/level2.txt",
            "level/level3.txt",
            "level/level4.txt",
            "level/level5.txt"
        ]

        level_loader = LevelLoader(level_files)
        level_loader.load_levels()

        game_engine = GameEngine(
            screen,
            max_level=len(level_files),
            level_loader=level_loader,
            music_enabled=args.music_enabled,
        )

        game_engine.run()

    except LevelFileError as e:
        print(f"Erro no nível: {e}")
    except pygame.error as e:
        print(f"Erro do pygame: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
