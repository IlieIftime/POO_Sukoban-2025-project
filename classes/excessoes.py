ELEMENTOS_VALIDOS = ['p', 'b', 's', 'o', '_']


class LevelFileError(Exception):
    """Classe da xcessão base para erros de ficheiro."""
    def __init__(self, message, linha, coluna, ficheiro):
        """
        Initialize the exception.

        Args:
            message (str): Mensagem descritiva do erro.
            linha (int): Linha do erro.
            coluna (int): Coluna do erro.
            ficheiro (str): Nome do ficheiro em que ocorre o erro.
        """
        super().__init__(f"{message} (Linha: {linha}, Coluna: {coluna}, Arquivo: {ficheiro})")
        self.linha = linha
        self.coluna = coluna
        self.ficheiro = ficheiro


class InvalidElementError(LevelFileError):
    """Classe para excessões relativas a elementos inválidos."""
    def __init__(self, elemento, linha, coluna, ficheiro):
        """
        Inicializa a classe.

        Args:
            elemento (str): Tipo de elemento inválido.
            linha (int): Linha do erro.
            coluna (int): Coluna do erro.
            ficheiro (str): Nome do ficheiro do erro.
        """
        super().__init__(f"Elemento inválido '{elemento}'", linha, coluna, ficheiro)


def verificar_elemento_invalido(linha, coluna, elemento, ficheiro):
    """
    Verica se um elemento é inválido.

    Raises:
        InvalidElementError: Se o elemento não for válido.
    """
    if elemento not in ELEMENTOS_VALIDOS:
        raise InvalidElementError(elemento, linha, coluna, ficheiro)


def verificar_linha_a_mais(linha, numero_elementos, index, ficheiro):
    """
    Verifica se existem elementos a mais no ficheiro.
    Raises:
        LevelFileError: Se contêm elemento a mais.
    """
    if len(linha) > numero_elementos:
        print(f"Linha com elementos a mais (Linha: {index}, Arquivo: {ficheiro}). Elementos extras ignorados.")
        return linha[:numero_elementos]  # Retorna a linha truncada
    return linha


def verificar_linha_incompleta(linha, numero_elementos, index, ficheiro):
    """
    Verifa se existem linhas incompletas.

    Raises:
        LevelFileError: Se existirem elementos a menos.
    """
    if len(linha) < numero_elementos:
        print(f"Linha com elementos a menos (Linha: {index}, Arquivo: {ficheiro}). Preenchendo espaços vazios ('_').")
        return linha.ljust(numero_elementos, "_")  # Preenche com '_'
    return linha


def verificar_elementos_obrigatorios(caixas, slots, ficheiro):
    """
    Verifa o nº de elementos obrigatórios.

    Raises:
        LevelFileError: Se o nº de caixas e slots for diferente.
    """
    if caixas != slots:
        raise LevelFileError(
            f"Número de caixas ({caixas}) diferente do número de slots ({slots})",
            0, 0, ficheiro
        )


def verificar_estrutura_geral(grid, ficheiro):
    """
    Verifa a estrutura geral da grid se corresponde com o esperado.


    Raises:
        LevelFileError: Se algum elemento não corresponder com as regras do nº de elementos.
    """
    elementos = [char for linha in grid for char in linha]
    player_count = elementos.count('p')
    box_count = elementos.count('b')
    slot_count = elementos.count('s')

    if player_count != 1:
        raise LevelFileError(
            f"Número inválido de jogadores (esperado 1, encontrado {player_count})",
            0, 0, ficheiro
        )
    if box_count != slot_count:
        raise LevelFileError(
            f"Número de caixas ({box_count}) diferente do número de slots ({slot_count})",
            0, 0, ficheiro
        )
    return box_count, slot_count
