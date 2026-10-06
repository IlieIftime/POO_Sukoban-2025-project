import pygame

class GameObject(pygame.sprite.Sprite):
    """Classe base para objetos do jogo."""

    def __init__(self, image, x, y):
        """Initialize the GameObject.

        Args:
            image (pygame.Surface): Superficie que representa a instância.
            x (int): Inicializa a coordenada x.
            y (int): Inicializa a coordenada y.
        Raises:
            ValueError: If the provided image is None.
        """
        super().__init__()
        if image is None:  # Valida a imagem providenciada
            raise ValueError("Imagem não pode ser None.")
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        """Desenha o objeto do jogo.

        Args:
            screen (pygame.Surface): Superficie onde o objeto será desenhado.
        """
        if not isinstance(screen, pygame.Surface):  # Valida o parâmetro screen
            raise TypeError("O parametro da tela tem de corresponder ao pygame.surface.")
        screen.blit(self.image, self.rect)

