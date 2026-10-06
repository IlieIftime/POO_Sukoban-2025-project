from classes.gameobject import GameObject

class StepableObject(GameObject):
    """Classe que representa um objeto que pode ser pisado ou interagido."""

    def __init__(self, image, x, y):
        """Inicializa o box spot.
            Args:
            x (int): Coordenada horizontal inicial.
            y (int): Coordenada vertical inicial.
            image (pygame.Surface): A imagem que representa o objeto.
        """
        super().__init__(image, x, y)
