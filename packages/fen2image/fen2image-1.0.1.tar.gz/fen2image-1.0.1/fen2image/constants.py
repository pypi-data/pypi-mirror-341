from pathlib import Path

# paths constants
PATH_PROJECT = Path(__file__).resolve().parent.parent
PATH_ARTS = PATH_PROJECT / 'resources' / 'arts'
PATH_BOARDS = PATH_ARTS / 'boards'
PATH_PIECES = PATH_ARTS / 'pieces'
PATH_OTHER = PATH_ARTS / 'other'
PATH_RESULT = PATH_PROJECT / 'result_file'

# dictionary associations
piece_to_filename = {
    "p": "bP.png",
    "r": "bR.png",
    "n": "bN.png",
    "b": "bB.png",
    "q": "bQ.png",
    "k": "bK.png",
    "P": "wP.png",
    "R": "wR.png",
    "N": "wN.png",
    "B": "wB.png",
    "Q": "wQ.png",
    "K": "wK.png",
}