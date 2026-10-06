from classes.obstacle import Obstacle

class PineTree(Obstacle):
    """Classe que representa um pinheiro como obstáculo no jogo."""

    def __init__(self, x, y):
        """Inicializa um pinheiro com posição e imagem específicas.

        Args:
            x (int): Coordenada horizontal inicial.
            y (int): Coordenada vertical inicial.
        Raises:
            FileNotFoundError: Se o arquivo da imagem não for encontrado.
        """
        image_path = 'images/pine.png'
        try:
            super().__init__(image_path, x, y)
        except FileNotFoundError:
            raise FileNotFoundError(f"Imagem do PineTree não encontrada: {image_path}")
