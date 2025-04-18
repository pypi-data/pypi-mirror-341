from .constants import *


def get_list_available_boards() -> list[str]:
    """
    List all available boards.

    :return: a list of available boards
    """
    return [_.name.split('.')[0] for _ in PATH_BOARDS.iterdir() if _.is_file()]

def get_list_available_pieces() -> list[str]:
    """
    List all available pieces.

    :return: a list of available pieces
    """
    return [_.name for _ in PATH_PIECES.iterdir()]

def get_dict_available_boards() -> dict[str, Path]:
    """
    List all available boards.

    :return: a dictionary of available boards with their name as key and their path as value
    """
    return {_.name.split('.')[0]: _ for _ in PATH_BOARDS.iterdir() if _.is_file()}

def get_dict_available_pieces() -> dict[str, Path]:
    """
    List all available pieces.

    :return: a dictionary of available pieces with their name as key and their path as value
    """
    return {_.name: _ for _ in PATH_PIECES.iterdir()}