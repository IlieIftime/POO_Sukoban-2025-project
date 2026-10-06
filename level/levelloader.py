import pygame
from classes.player import Player
from classes.box import Box
from classes.boxspot import BoxSpot
from classes.obstacle import Obstacle
from classes.excessoes import (
    InvalidElementError,
    LevelFileError,
    verificar_elemento_invalido,
    verificar_linha_a_mais,
    verificar_linha_incompleta,
    verificar_elementos_obrigatorios,
    verificar_estrutura_geral,
)
from collection.imagecollection import ImageCollection


class LevelLoader:
    """Classe para carregar os níveis do jogo Sokoban."""

    def __init__(self, filenames, grid_size=(10, 10)):
        """
            Inicializa o carregador de níveis.

        Args:
            filenames (list): Lista de caminhos para os arquivos de níveis.
            grid_size (tuple): Dimensões da grade do nível (linhas, colunas).
        Raises:
            FileNotFoundError: Se algum arquivo não for encontrado.
        """
        self.filenames = filenames
        self.grid_size = grid_size
        self.levels = {}  # Dicionario para armazenar os níveis
        self.image_collection = ImageCollection()
        self.image_collection.load_images()

        if not pygame.image.get_extended():  # Verificar se o Pygame suporta formatos de imagem estendidos
            raise RuntimeError("Pygame não suporta formatos de imagem estendidos.")

    def load_levels(self):
        """Carrega todos os níveis apartir de aquivos .txt"""
        print("Carregando níveis...")  # Debug message
        for idx, filename in enumerate(self.filenames, start=1):
            try:
                level_name = f"Level {idx}"
                level_data = self.load_single_level(filename)
                self.levels[level_name] = level_data
            except (InvalidElementError, LevelFileError) as e:
                print(f"Erro no arquivo '{filename}': {e}")
        print("Níveis carregados:", self.levels.keys())

    def load_single_level(self, filename):
        """
        Carrega e processa um único arquivo de nível.

        Args:
            filename (str): Caminho para o arquivo do nível.
        Returns:
            dict: Um dicionário contendo a grade e os objetos do nível.
        """
        level_data = {
            "grid": [],
            "player": None,
            "boxes": [],
            "obstacles": [],
            "box_spots": [],
        }

        try:
            with open(filename, "r") as file:
                grid = []
                player_positions = []
                box_positions = []
                slot_positions = []

                for line_number, line in enumerate(file):
                    # Verificar e corrigir linhas com elementos extras ou faltando
                    line = verificar_linha_a_mais(line.strip(), self.grid_size[1], line_number + 1, filename)
                    line = verificar_linha_incompleta(line, self.grid_size[1], line_number + 1, filename)

                    # Verificar cada caractere da linha
                    for column_number, char in enumerate(line):
                        verificar_elemento_invalido(line_number + 1, column_number + 1, char, filename)

                        # Coletar as posições para validações adicionais
                        if char == "p":
                            player_positions.append((line_number + 1, column_number + 1))
                        elif char == "b":
                            box_positions.append((line_number + 1, column_number + 1))
                        elif char == "s":
                            slot_positions.append((line_number + 1, column_number + 1))

                    grid.append(line)

                # Verificar estrutura geral do nível
                box_count, slot_count = len(box_positions), len(slot_positions)
                self._validate_structure(player_positions, box_positions, slot_positions, filename)

                # Processar o grid para criar objetos
                for row_index, row in enumerate(grid):
                    for col_index, char in enumerate(row):
                        x = col_index * 50
                        y = row_index * 50
                        if char == "p":
                            level_data["player"] = Player(self.image_collection.get_image("player_right"), x, y)
                        elif char == "b":
                            level_data["boxes"].append(Box(self.image_collection.get_image("box"), x, y))
                        elif char == "s":
                            level_data["box_spots"].append(BoxSpot(self.image_collection.get_image("box_spot"), x, y))
                        elif char == "o":
                            level_data["obstacles"].append(Obstacle(self.image_collection.get_image("pinetree"), x, y))

                level_data["grid"] = grid

        except LevelFileError as e:
            print(f"Erro ao carregar o nível: {e}")
            pygame.quit()
            exit()
        except InvalidElementError as e:
            print(f"Erro de elemento inválido: {e}")
            pygame.quit()
            exit()
        except Exception as e:
            print(f"Erro inesperado ao carregar o nível: {e}")
            pygame.quit()
            exit()

        return level_data

    def _validate_structure(self, player_positions, box_positions, slot_positions, filename):
        """
          Valida a estrutura da grade do nível.

        Args:
            player_positions (list): Lista de posições do jogador na grade.
            box_positions (list): Lista de posições das caixas na grade.
            slot_positions (list): Lista de posições dos slots na grade.
            filename (str): Nome do arquivo do nível.

        Raises:
            LevelFileError: Se qualquer problema estrutural for encontrado no nível.
        """
        # Verificar o número de jogadores
        if len(player_positions) != 1:
            for pos in player_positions:
                print(f"Jogador duplicado encontrado em (Linha: {pos[0]}, Coluna: {pos[1]}).")
            raise LevelFileError(
                f"Número inválido de jogadores. Esperado: 1, Encontrado: {len(player_positions)}",
                player_positions[0][0] if player_positions else 0,
                player_positions[0][1] if player_positions else 0,
                filename,
            )

        # Verificar o número de caixas e slots
        if len(box_positions) == 0 and len(slot_positions) == 0:
            raise LevelFileError(
                f"Nenhuma caixa ou slot encontrado no nível.",
                0,
                0,
                filename,
            )

        if len(box_positions) != len(slot_positions):
            for pos in box_positions + slot_positions:
                print(f"Caixa ou slot em conflito encontrado em (Linha: {pos[0]}, Coluna: {pos[1]}).")
            raise LevelFileError(
                f"Número de caixas ({len(box_positions)}) diferente do número de slots ({len(slot_positions)})",
                0,
                0,
                filename,
            )

    def draw(self, screen, level_name=None):
        """
        Desenha um nível específico na tela.

        Args:
            screen (pygame.Surface): Superfície onde os objetos serão desenhados.
            level_name (str, optional): Nome do nível a ser desenhado. Padrão: primeiro nível carregado.
        Raises:
            ValueError: Se nenhum nível foi carregado ou se o nível especificado não existe.
        """
        if not self.levels:
            raise ValueError("Não foram carregados níveis.")

        # usa nome default se não for especificado
        if level_name is None:
            level_name = list(self.levels.keys())[0]

        if level_name not in self.levels:
            raise ValueError(f"Level '{level_name}' não existe: {list(self.levels.keys())}")

        level_data = self.levels[level_name]

        # Desenha a grid
        for y, line in enumerate(level_data["grid"]):
            for x, char in enumerate(line):
                screen.blit(self.image_collection.get_image("land"), (x * 50, y * 50))

        # Desenha os objetos
        for slot in level_data["box_spots"]:
            slot.draw(screen)
        for obstacle in level_data["obstacles"]:
            obstacle.draw(screen)
        for box in level_data["boxes"]:
            box.draw(screen)
        if level_data["player"]:
            level_data["player"].draw(screen)

    def is_level_complete(self, level_name):
        """
         Verifica se um nível está completo.

        Args:
            level_name (str): Nome do nível a verificar.

        Returns:
            bool: True se todas as caixas estiverem nos slots, False caso contrário.
        """
        level_data = self.levels[level_name]
        return all(
            any(box.rect.topleft == slot.rect.topleft for slot in level_data["box_spots"])
            for box in level_data["boxes"]
        )
