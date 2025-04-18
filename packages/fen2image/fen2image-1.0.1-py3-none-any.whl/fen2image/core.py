from .Fen import Fen
from PIL import Image


def fen2image(fen: str, board_design: str = "random") -> Image:
    """
    Convert a FEN string to an image.

    :param:
        fen: the FEN string
        board_design: the design of the board as a string
    :return: the image
    """

    fen = Fen(fen)
    board = fen.to_board_representation()
    return board.create_image(board_design=board_design)