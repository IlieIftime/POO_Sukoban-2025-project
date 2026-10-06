from classes.stepableobject import StepableObject

class BoxSpot(StepableObject):
    """Classe que representa objetos que podem ser pisados ou interagidos"""

    def __init__(self, image, x, y):
        """Inicializa um objeto pisável com uma imagem e posição.

    Args:
        x (int): Posição horizontal inicial.
        y (int): Posição vertical inicial.
        image (pygame.Surface): A imagem que representa o objeto.

        """
        super().__init__(image, x, y)
        self.occupied = False  # Marks if the slot is occupied by a box

    def is_occupied(self):
        """Verifica se tem um slot ocupado pela caixa.

        Returns:
            bool: True se afirmativo, False caso contrario.
        """
        return self.occupied

    def set_occupied(self, status):
        """Set da posição ocupada.

        Args:
            True se os slots tiverem ocupados.
        Raises:
            TypeError: Se o status não for um booleano.
        """
        if not isinstance(status, bool):  # Valida o tipo de status
            raise TypeError("O slot ocupado deve ser um booleano.")
        self.occupied = status
