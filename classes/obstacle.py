from classes.gameobject import GameObject

class Obstacle(GameObject):
    """Classe que representa um obstáculo na grade do jogo."""

    def __init__(self, image, x, y):
        """Inicializa um obstáculo com uma imagem e posição.

        Args:
            image (pygame.Surface): Superfície da imagem do obstáculo.
            x (int): Coordenada horizontal inicial.
            y (int): Coordenada vertical inicial.
        Raises:
            ValueError: Se a imagem fornecida for None.
        """
        if image is None:  # Verifica se a imagem do obstáculo é válida
            raise ValueError("A imagem do obstáculo não pode ser None.")
        super().__init__(image, x, y)
