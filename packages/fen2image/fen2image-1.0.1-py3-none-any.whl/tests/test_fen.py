import unittest

from fen2image.Fen import Fen
from fen2image.BoardRepresentation import BoardRepresentation


class TestFen(unittest.TestCase):

    def setUp(self):
        self.valid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.invalid_structure_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0"
        self.invalid_ranks_fen = "rnbqkbnr/pppppppp/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.invalid_active_color = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1"
        self.invalid_castling = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQxq - 0 1"
        self.invalid_en_passant = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq i9 0 1"
        self.invalid_halfmove = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1"
        self.invalid_fullmove = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

    def test_str_and_repr(self):
        fen_obj = Fen(self.valid_fen)
        self.assertEqual(str(fen_obj), self.valid_fen)
        self.assertEqual(repr(fen_obj), self.valid_fen)

    def test_verify_valid_fen(self):
        fen_obj = Fen(self.valid_fen)
        try:
            fen_obj.verify()
        except Exception as e:
            self.fail(f"verify() raised an exception on a valid FEN: {e}")
        self.assertTrue(fen_obj.verified)

    def test_verify_invalid_structure(self):
        fen_obj = Fen(self.invalid_structure_fen)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect number of fields", str(context.exception))

    def test_verify_invalid_ranks(self):
        fen_obj = Fen(self.invalid_ranks_fen)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect number of ranks", str(context.exception))

    def test_verify_invalid_active_color(self):
        fen_obj = Fen(self.invalid_active_color)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect active color", str(context.exception))

    def test_verify_invalid_castling(self):
        fen_obj = Fen(self.invalid_castling)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect castling rights", str(context.exception))

    def test_verify_invalid_en_passant(self):
        fen_obj = Fen(self.invalid_en_passant)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect en passant target square", str(context.exception))

    def test_verify_invalid_halfmove(self):
        fen_obj = Fen(self.invalid_halfmove)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect half-move clock", str(context.exception))

    def test_verify_invalid_fullmove(self):
        fen_obj = Fen(self.invalid_fullmove)
        with self.assertRaises(ValueError) as context:
            fen_obj.verify()
        self.assertIn("Incorrect full-move number", str(context.exception))

    def test_to_board_representation_valid(self):
        fen_obj = Fen(self.valid_fen)
        fen_obj.verify()
        board_rep = fen_obj.to_board_representation()
        self.assertIsInstance(board_rep, BoardRepresentation)

        expected_board = [
            list("rnbqkbnr"),
            list("pppppppp"),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("PPPPPPPP"),
            list("RNBQKBNR")
        ]
        self.assertEqual(board_rep.board, expected_board)

        self.assertEqual(board_rep.color_turn, "w")
        self.assertEqual(board_rep.castling_rights, "KQkq")
        self.assertEqual(board_rep.en_passant, "-")
        self.assertEqual(board_rep.half_move_count, 0)
        self.assertEqual(board_rep.full_move_count, 1)

    def test_verify_called_multiple_times(self):
        fen_obj = Fen(self.valid_fen)
        fen_obj.verify()
        self.assertTrue(fen_obj.verified)
        try:
            fen_obj.verify()
        except Exception as e:
            self.fail(f"Second call to verify() raised an exception: {e}")
        self.assertTrue(fen_obj.verified)

    def test_valid_no_castling(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
        fen_obj = Fen(fen)
        fen_obj.verify()
        board_rep = fen_obj.to_board_representation()
        self.assertEqual(board_rep.castling_rights, "-")

    def test_valid_en_passant(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e3 0 1"
        fen_obj = Fen(fen)
        fen_obj.verify()
        board_rep = fen_obj.to_board_representation()
        self.assertEqual(board_rep.en_passant, "e3")

    def test_numeric_fields_conversion(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 15 30"
        fen_obj = Fen(fen)
        fen_obj.verify()
        board_rep = fen_obj.to_board_representation()
        self.assertEqual(board_rep.half_move_count, 15)
        self.assertEqual(board_rep.full_move_count, 30)


if __name__ == '__main__':
    unittest.main()
