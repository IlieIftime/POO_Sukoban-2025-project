import pygame
import os
from classes.excessoes import LevelFileError  # Importação de exceção personalizada

class ImageCollection:
    """Classe para carregar e gerenciar as imagens do jogo."""

    def __init__(self, base_path='images'):
        """Inicializa a coleção de imagens.

        Args:
            base_path (str): Caminho base para a pasta de imagens.
        Raises:
            LevelFileError: Se o diretório base das imagens não existir.
        """
        if not os.path.exists(base_path):
            raise LevelFileError("O diretório de imagens não existe", 0, base_path)
        self.base_path = base_path
        self.images = {
            'box': None,
            'box_spot': None,
            'player_left': None,
            'player_right': None,
            'land': None,
            'pinetree': None
        }

    def load_images(self):
        """Carrega todas as imagens necessárias e armazena nos atributos."""
        try:
            self.images['box'] = self._load_image('box.png')
            self.images['box_spot'] = self._load_image('box_spot.png')
            self.images['player_left'] = self._load_image('player.png')
            self.images['player_right'] = self._load_image('player_right.png')
            self.images['land'] = self._load_image('land.png')
            self.images['pinetree'] = self._load_image('pine.png')
            # Resize the box_spot image to 50x50
            self.images["box_spot"] = pygame.transform.scale(self.images["box_spot"], (50, 50))
        except FileNotFoundError as e:
            raise LevelFileError(f"Erro ao carregar imagem: {e}", 0, self.base_path)

    def get_image(self, name):
        """Retorna a imagem solicitada pelo nome.

        Args:
            name (str): Nome da imagem na coleção.

        Returns:
            pygame.Surface: Objeto da imagem carregada.

        Raises:
            KeyError: Se o nome da imagem não existir na coleção.
        """
        if name not in self.images:
            raise KeyError(f"Imagem '{name}' não encontrada na coleção.")
        return self.images.get(name)

    def _load_image(self, filename):
        """Carrega uma imagem do caminho base.

        Args:
            filename (str): Nome do arquivo da imagem.

        Returns:
            pygame.Surface: Objeto da imagem carregada.

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado.
        """
        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Imagem não encontrada: {path}")
        return pygame.image.load(path).convert_alpha()
