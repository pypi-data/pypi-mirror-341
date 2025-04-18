import unittest
from pathlib import Path
from unittest.mock import patch
from fen2image.BoardRepresentation import BoardRepresentation


class TestBoardRepresentation(unittest.TestCase):

    def setUp(self):
        # Create a sample board representation (an 8x8 board)
        self.sample_board = [
            list("rnbqkbnr"),
            list("pppppppp"),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("PPPPPPPP"),
            list("RNBQKBNR")
        ]
        self.color_turn = "w"
        self.castling_rights = "KQkq"
        self.en_passant = "-"
        self.half_move_count = 0
        self.full_move_count = 1

        self.br = BoardRepresentation(
            board=self.sample_board,
            color_turn=self.color_turn,
            castling_rights=self.castling_rights,
            en_passant=self.en_passant,
            half_move_count=self.half_move_count,
            full_move_count=self.full_move_count
        )

    def test_initialization(self):
        """Test that the attributes are correctly stored upon initialization."""
        self.assertEqual(self.br.board, self.sample_board)
        self.assertEqual(self.br.color_turn, self.color_turn)
        self.assertEqual(self.br.castling_rights, self.castling_rights)
        self.assertEqual(self.br.en_passant, self.en_passant)
        self.assertEqual(self.br.half_move_count, self.half_move_count)
        self.assertEqual(self.br.full_move_count, self.full_move_count)

    @patch("fen2image.BoardRepresentation.get_list_available_pieces", return_value=["classic", "modern"])
    @patch("fen2image.BoardRepresentation.get_list_available_boards", return_value=["wood", "metal"])
    def test_verify_designs_valid(self, mock_boards_list, mock_pieces_list):
        """Test that _verify_designs passes with valid design names."""
        try:
            self.br._verify_designs("classic", "wood")
        except ValueError as e:
            self.fail(f"_verify_designs raised ValueError unexpectedly: {e}")

    @patch("fen2image.BoardRepresentation.get_list_available_pieces", return_value=["classic", "modern"])
    def test_verify_designs_invalid_pieces(self, mock_pieces_list):
        """Test that _verify_designs raises an error for an invalid pieces design."""
        with self.assertRaises(ValueError) as context:
            self.br._verify_designs("invalid_design", "wood")
        self.assertIn("Pieces design 'invalid_design' is not available", str(context.exception))

    @patch("fen2image.BoardRepresentation.get_list_available_boards", return_value=["wood", "metal"])
    def test_verify_designs_invalid_board(self, mock_boards_list):
        """Test that _verify_designs raises an error for an invalid board design."""
        with self.assertRaises(ValueError) as context:
            self.br._verify_designs("classic", "invalid_board")
        self.assertIn("Board design 'invalid_board' is not available", str(context.exception))

    @patch("fen2image.BoardRepresentation.get_dict_available_boards", return_value={"wood": "dummy_board_path.png", "metal": "dummy_board_path2.png"})
    @patch("fen2image.BoardRepresentation.get_dict_available_pieces", return_value={"classic": Path("dummy_pieces"), "modern": Path("dummy_pieces_mod")})
    @patch("fen2image.BoardRepresentation.get_list_available_pieces", return_value=["classic", "modern"])
    @patch("fen2image.BoardRepresentation.get_list_available_boards", return_value=["wood", "metal"])
    @patch.dict("fen2image.constants.piece_to_filename", {"P": "wP.png", "p": "bP.png", "K": "wK.png", "k": "bK.png"})
    def test_create_image_piece_pasting(self, mock_dict_boards, mock_dict_pieces, mock_list_pieces, mock_list_boards):
        """
        Test a scenario where the board has an actual piece so that the paste() function is called.
        We create a board with one white pawn ('P') placed in the 3rd row.
        """
        board_with_piece = [
            list("........"),
            list("........"),
            list("....P..."),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("........")
        ]
        br_with_piece = BoardRepresentation(
            board=board_with_piece,
            color_turn="w",
            castling_rights="-",
            en_passant="-",
            half_move_count=0,
            full_move_count=1
        )

    @patch("fen2image.BoardRepresentation.get_dict_available_boards", return_value={"wood": "dummy_board_path.png", "metal": "dummy_board_path2.png"})
    @patch("fen2image.BoardRepresentation.get_dict_available_pieces", return_value={"classic": Path("dummy_pieces"), "modern": Path("dummy_pieces_mod")})
    @patch("fen2image.BoardRepresentation.get_list_available_pieces", return_value=["classic", "modern"])
    @patch("fen2image.BoardRepresentation.get_list_available_boards", return_value=["wood", "metal"])
    def test_create_image_invalid_designs(self, mock_boards_list, mock_pieces_list, mock_dict_pieces, mock_dict_boards):
        """
        Test that create_image raises a ValueError when given an unavailable pieces or board design.
        """
        with self.assertRaises(ValueError) as context:
            self.br.create_image(pieces_design="nonexistent", board_design="wood")
        self.assertIn("Pieces design 'nonexistent' is not available", str(context.exception))

        with self.assertRaises(ValueError) as context2:
            self.br.create_image(pieces_design="classic", board_design="nonexistent")
        self.assertIn("Board design 'nonexistent' is not available", str(context2.exception))


if __name__ == '__main__':
    unittest.main()
