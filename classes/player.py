import pygame
from classes.movableobject import MovableObject

class Player(MovableObject):
    """Class representing the player in the Sokoban game."""

    def __init__(self, image, x, y):
        """Inicializa o jogador com uma imagem e posição.

        Args:
        image (pygame.Surface): Superfície para a imagem do jogador.
        x (int): Posição horizontal inicial.
        y (int): Posição vertical inicial.

        """
        super().__init__(x, y, image)
        self.steps = 0  # contador de passos
        self.direction = 'right'  # posição inicial
        self.previous_position = (x, y) # Guarda a posição inicial
        self.start_x, self.start_y = x, y  # Guarda a posição inicial

    def move(self, dx, dy, obstacles, boxes, grid_size=(500, 500)):
        """Move o jogador na direção especificada.

    Args:
        dx (int): Movimento horizontal (-1 para esquerda, 1 para direita).
        dy (int): Movimento vertical (-1 para cima, 1 para baixo).
        obstacles (list): Lista de obstáculos no jogo.
        boxes (list): Lista de caixas no jogo.
        grid_size (tuple): Tamanho da grade do jogo (largura, altura).

    Returns:
        bool: True se o movimento for bem-sucedido, False caso contrário
        """
        # Atualiza a direção e a imagem do jogador com base no movimento
        self._update_direction_and_image(dx)

        # Calcula nova posição
        new_x, new_y = self.rect.x + dx * 50, self.rect.y + dy * 50

        #Verifica se a nova posição está dentro dos limites
        if not self._is_within_bounds(new_x, new_y, grid_size):
            return False

        # Verifica se há colisão com obstáculos
        if self._has_collision(new_x, new_y, obstacles, []):
            return False

        # Verifica se há colisão com caixas
        for box in boxes:
            if box.rect.collidepoint(new_x, new_y):
                if box.push(dx, dy, obstacles, boxes, grid_size):  # Attempt to push the box
                    self._update_position(new_x, new_y)
                    return True
                return False

        # Atualiza a posição do jogador se não houver colisões
        self._update_position(new_x, new_y)
        return True

    def set_image(self, image_path):
        """Atualiza a imagem do jogador.

        Args:
            image_path (str): Caminho para a nova imagem do jogador.
        Raises:
        FileNotFoundError: Se o caminho da imagem não for encontrado

        """
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except FileNotFoundError:
            raise FileNotFoundError(f"Imagem do jogador não encontrada: {image_path}")

    def _update_direction_and_image(self, dx):
        """Atualiza a direção e a imagem do jogador com base no movimento.

    Args:
        dx (int): Movimento horizontal (-1 para esquerda, 1 para direita).

        """
        if dx > 0:
            self.set_image('images/player_right.png')
            self.direction = 'right'
        elif dx < 0:
            self.set_image('images/player.png')
            self.direction = 'left'

    def _update_position(self, x, y):
        """Atualiza a posição do jogador e incrementa o contador de passos.

    Args:
        x (int): Nova posição x.
        y (int): Nova posição y.

        """
        self.previous_position = (self.rect.x, self.rect.y)
        self.rect.x, self.rect.y = x, y
        self.steps += 1

    def reset_position(self):
        """Reseta o jogador para a posição inicial."""
        self.rect.topleft = (self.start_x, self.start_y)
        print(f"Jogador resetado para posição inicial: ({self.start_x}, {self.start_y})")