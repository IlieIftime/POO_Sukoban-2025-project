import pygame
from classes.excessoes import LevelFileError
from classes.player import Player
from classes.box import Box
from classes.boxspot import BoxSpot

class Level:
    """Classe que lida com elementos do jogo."""

    def __init__(self, player=None):
        """Inicializa um nivel.

        Args:
            player (Player, optional): O jogador representado, default é None.
        Raises:
            LevelFileError: Se o jogador não for válido.
        """
        if player and not isinstance(player, Player):
            raise LevelFileError("O jogador providenciado não é uma instância valida.", 0, "Level")
        self.__player = player
        self.__immovable_objects = pygame.sprite.Group()
        self.__movable_objects = pygame.sprite.Group()
        self.__boxspot_objects = pygame.sprite.Group()

    def set_player(self, player):
        """Carrega o jogador.

        Args:
            player (Player): Jogador associado ao jogo.
        Raises:
            LevelFileError: Se o jogador não for válido.
        """
        if not isinstance(player, Player):
            raise LevelFileError("Jogador providenciado não é uma instância válida.", 0, "Level")
        self.__player = player

    def get_player(self):
        """obtêm o jogador associado ao jogo.

        Returns:
            Player: O jogador associado ao nível.
        """
        return self.__player

    def add_immovable(self, obj):
        """Adiciona objeto imovivel.

        Args:
            obj (GameObject): Objeto imovivel.
        Raises:
            LevelFileError: Se o objeto não for válido.
        """
        if not isinstance(obj, pygame.sprite.Sprite):
            raise LevelFileError("Instância de objeto imovivel não válida.", 0, "Level")
        self.__immovable_objects.add(obj)

    def get_immovables(self):
        """Obtem os imoviveis.

        Returns:
            pygame.sprite.Group: Grupo sprite.pygame.
        """
        return self.__immovable_objects

    def add_movable(self, obj):
        """Adiciona os objetos moviveis.

        Args:
            obj (MovableObject): Objetos moviveis.
        Raises:
            LevelFileError: Se o objeto não for válido.
        """
        if not isinstance(obj, Box):  # O objeto movivel é uma caixa
            raise LevelFileError("Objeto movivel não válido.", 0, "Level")
        self.__movable_objects.add(obj)

    def get_movables(self):
        """Obtem os objetos moviveis.

        Returns:
            pygame.sprite.Group: Grupo pygame.sprite.
        """
        return self.__movable_objects

    def add_boxspot(self, obj):
        """Adiciona os box spots.

        Args:
            obj (BoxSpot): Slots a adicionar.
        Raises:
            LevelFileError: Se o objeto não for válido.
        """
        if not isinstance(obj, BoxSpot):
            raise LevelFileError("Instância da box slot não válida", 0, "Level")
        self.__boxspot_objects.add(obj)

    def get_boxspots(self):
        """Obtem os boxspots.

        Returns:
            pygame.sprite.Group: Grupo pygame.sprite.
        """
        return self.__boxspot_objects


######adicionar decorador para os getters pelo menos 1
#########projeto todo pelo menos 1 decorador
######## ideal mais que um
########ver isto na 5º feira