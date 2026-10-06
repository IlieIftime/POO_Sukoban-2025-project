import pygame
import time
from level.levelloader import LevelLoader
from collection.imagecollection import ImageCollection
from classes.excessoes import LevelFileError, InvalidElementError


def ensure_valid_level(func):
    """Decorador para garantir que o nível atual é válido antes de executar a função."""
    def wrapper(self, *args, **kwargs):
        level_name = f"Level {self.current_level}"
        if level_name not in self.level_loader.levels:
            raise ValueError(f"O nível '{level_name}' não foi encontrado.")
        return func(self, *args, **kwargs)
    return wrapper


class GameEngine:
    """Classe que gerencia a execução principal do jogo Sokoban."""

    def __init__(self, screen, max_level, level_loader, music_enabled=False):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("O parâmetro 'screen' deve ser uma instância de pygame.Surface.")
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.game_size = 500
        self.game_surface = pygame.Surface((self.game_size, self.game_size))
        self.max_level = max_level
        self.music_enabled = music_enabled
        self.current_level = 1
        self.level_loader = level_loader
        self.is_paused = False
        self.steps = 0
        self.total_steps = 0
        self.total_time = 0
        self.font = pygame.font.Font(None, 36)
        self.start_time = None
        self.image_collection = ImageCollection()
        self.image_collection.load_images()
        self.background = self._create_background(self.image_collection.get_image('land'))

    def _create_background(self, land_texture):
        """Cria uma superfície de background de 500x500 com textura "land"."""
        if not isinstance(land_texture, pygame.Surface):
            raise ValueError("A textura do terreno deve ser uma instância de pygame.Surface.")
        background = pygame.Surface((self.game_size, self.game_size))
        for row in range(10):
            for col in range(10):
                x = col * 50
                y = row * 50
                background.blit(land_texture, (x, y))
        return background

    @ensure_valid_level
    def load_level(self):
        """Carrega o nível atual do jogo usando o LevelLoader."""
        try:
            level_name = f"Level {self.current_level}"
            print(f"Carregando {level_name}...")
            self.steps = 0
            self.start_time = time.time()

            # Carregar os dados do nível usando o LevelLoader
            level_data = self.level_loader.levels[level_name]

            # Configurar elementos do nível
            self.player = level_data["player"]
            self.boxes = level_data["boxes"]
            self.obstacles = level_data["obstacles"]
            self.box_spots = level_data["box_spots"]

        except (FileNotFoundError, LevelFileError, InvalidElementError, ValueError) as e:
            print(f"Erro ao carregar o nível: {e}")
            pygame.quit()
            exit()

    @ensure_valid_level
    def reset_level(self):
        """Reinicia o nível atual, redefinindo posições do jogador e caixas."""
        print(f"Reiniciando o nível {self.current_level}...")
        level_name = f"Level {self.current_level}"
        level_data = self.level_loader.levels[level_name]

        # Reset da posição do jogador
        level_data["player"].reset_position()

        # Reset das posições das caixas
        for box in level_data["boxes"]:
            box.reset_position()

        # Recarregar o nível
        self.load_level()

    def next_level(self):
        """Passa para o próximo nível, ou exibe a pontuação final ao concluir todos os níveis."""
        level_time = int(time.time() - self.start_time)
        self.total_steps += self.steps
        self.total_time += level_time

        if self.current_level < self.max_level:
            self.current_level += 1
            self.load_level()
        else:
            self.show_final_score()

    def show_final_score(self):
        """Exibe a pontuação final ao concluir todos os níveis."""
        print("Jogo concluído! Parabéns!")
        print(f"Passos totais: {self.total_steps}")
        print(f"Tempo total: {self.total_time} segundos")
        pygame.quit()
        exit()

    def run(self):
        """Executa o loop principal do jogo."""
        self.load_level()
        clock = pygame.time.Clock()

        if self.music_enabled:
            pygame.mixer.init()
            pygame.mixer.music.load("lamusica.mp3")
            pygame.mixer.music.play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("Tecla 'R' pressionada. Reiniciando o nível...")
                        self.reset_level()
                    elif event.key == pygame.K_p:
                        self.is_paused = not self.is_paused
                    elif not self.is_paused:
                        self._handle_player_movement(event.key)

            if not self.is_paused:
                self.game_surface.blit(self.background, (0, 0))
                level_name = f"Level {self.current_level}"
                self.level_loader.draw(self.game_surface, level_name)
                elapsed_time = int(time.time() - self.start_time)
                self._display_status(self.game_surface, elapsed_time)
                scaled_surface = pygame.transform.scale(self.game_surface, (self.screen_width, self.screen_height))
                self.screen.blit(scaled_surface, (0, 0))

                if self.level_loader.is_level_complete(level_name):
                    self.next_level()

                pygame.display.flip()
                clock.tick(30)

        if self.music_enabled:
            pygame.mixer.music.stop()

    def _handle_player_movement(self, key):
        """Lida com o movimento do jogador com base nas teclas pressionadas."""
        try:
            if key in (pygame.K_LEFT, pygame.K_a):
                moved = self.player.move(-1, 0, self.obstacles, self.boxes)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                moved = self.player.move(1, 0, self.obstacles, self.boxes)
            elif key in (pygame.K_UP, pygame.K_w):
                moved = self.player.move(0, -1, self.obstacles, self.boxes)
            elif key in (pygame.K_DOWN, pygame.K_s):
                moved = self.player.move(0, 1, self.obstacles, self.boxes)
            else:
                moved = False

            if moved:
                self.steps += 1
        except Exception as e:
            print(f"Erro ao mover o jogador: {e}")

    def _display_status(self, surface, elapsed_time):
        """Exibe o status de passos e tempo na tela."""
        steps_text = self.font.render(f"Passos: {self.steps}", True, (255, 255, 255))
        time_text = self.font.render(f"Tempo: {elapsed_time}s", True, (255, 255, 255))
        surface.blit(steps_text, (10, 10))
        surface.blit(time_text, (10, 40))
