from classes.gameobject import GameObject

class MovableObject(GameObject):
    """Classe base para objectos que se movem."""

    def __init__(self, x, y, image):
        """Inicializa o objeto movivel e a sua imagem e coordenadas.

        Args:
            x (int): Inicializa a coordenada x.
            y (int): Inicializa a coordenada y.
            image (pygame.Surface): Representa a imagem.
        """
        super().__init__(image, x, y)

    def move(self, dx, dy, grid, grid_size=(500, 500)):
        """Empurra o objeto para nova posição se possível.

        Args:
            dx (int): Horizontal movement (-1 para esquerda, 1 para direita).
            dy (int): Vertical movement (-1 para cima, 1 para baixo).
            grid: Objeto na grelha.
            grid_size (tuple): Tamanho da tela 500x500 por default.

        Returns:
            bool: True se o movimento for efectuado.
        """
        # Calcula nova posição
        new_x = self.rect.x + dx * 50
        new_y = self.rect.y + dy * 50

        # Verifica se a nova posição está dentro dos limites
        if not self._is_within_bounds(new_x, new_y, grid_size):
            return False

        # Verifica se há colisão com obstáculos
        if grid.is_position_valid(new_x // 50, new_y // 50):
            self.rect.x = new_x
            self.rect.y = new_y
            return True

        return False

    def _is_within_bounds(self, x, y, grid_size):
        """verifica se as posições estão dentro dos imites.

        Args:
            x (int): nova posição x.
            y (int): nova posição y.
            grid_size (tuple): Tamanho da tela.

        Returns:
            bool: True se a posição estiver dentro dos limites, False caso contrário.
        """
        width, height = grid_size
        return 0 <= x < width and 0 <= y < height

    def _has_collision(self, new_x, new_y, obstacles, others):
        """Verifica colisões.

        Args:
            new_x (int): Nova posição x.
            new_y (int): Nova posição y.
            obstacles (list): Lists de obstaculos.
            others (list): Lista de outros obstaculos a serem considerados para colisão.

        Returns:
            bool: True se existir colisão.
        """
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(new_x, new_y):
                return True  # Colisão com outro objeto
        for other in others:
            if other != self and other.rect.collidepoint(new_x, new_y):
                return True  # Colisão com outro objeto
        return False
