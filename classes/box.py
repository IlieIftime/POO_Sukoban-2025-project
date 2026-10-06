from classes.movableobject import MovableObject

class Box(MovableObject):
    """Classe que representa as caixas."""

    def __init__(self, image, x, y):
        """Initialize a box with an image and position.

        Args:
             image (pygame.Surface): Superfície para a imagem da caixa.
        x (int): Posição horizontal inicial.
        y (int): Posição vertical inicial.
        """
        super().__init__(x, y, image)
        self.previous_position = self.rect.topleft  # Store the initial position
        self.start_x, self.start_y = x, y  # Store the initial position

    def push(self, dx, dy, obstacles, boxes, grid_size=(500, 500)):
        """Empurra a caixa em uma direção específica, se possível
           Args:
        dx (int): Movimento horizontal (-1 para esquerda, 1 para direita).
        dy (int): Movimento vertical (-1 para cima, 1 para baixo).
        obstacles (list): Lista de obstáculos no jogo.
        boxes (list): Lista de outras caixas no jogo.
        grid_size (tuple): Tamanho da grade do jogo (largura, altura).

    Returns:
        bool: True se o movimento for realizado, False caso contrário.

        """
        # Calcula nova posição da caixa
        new_x, new_y = self.rect.x + dx * 50, self.rect.y + dy * 50

        #Verifica se a nova posição está dentro dos limites
        if not self._is_within_bounds(new_x, new_y, grid_size):
            return False

        # Verifica se há colisão com obstáculos
        if self._has_collision(new_x, new_y, obstacles, boxes):
            return False

        # Move a caixa para a nova posição se não houver colisões
        self.previous_position = self.rect.topleft
        self.rect.x, self.rect.y = new_x, new_y
        return True

    def reset_position(self):
        """Reseta o jogador para a posição inicial."""
        self.rect.topleft = (self.start_x, self.start_y)
        print(f"Jogador resetado para posição inicial: ({self.start_x}, {self.start_y})")