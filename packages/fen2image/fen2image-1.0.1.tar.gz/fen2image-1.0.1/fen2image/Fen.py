from .BoardRepresentation import BoardRepresentation


class Fen:

    def __init__(self, fen: str) -> None:
        """
        Initializes the Fen object with a FEN string.

        :param fen: The FEN string to be managed.
        """
        self.fen = fen
        self.verified = False

    def __str__(self) -> str:
        """
        Returns the FEN string.

        :return: The FEN string.
        """
        return self.fen

    def __repr__(self) -> str:
        """
        Returns the FEN string.

        :return: The FEN string.
        """
        return self.fen

    def to_board_representation(self) -> BoardRepresentation:
        """
        Convert FEN object to a BoardRepresentation object.
        """
        if not self.verified:
            self.verify()

        split_fen = self.fen.split(" ")

        board = []
        rows = split_fen[0].split('/')
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend(['.'] * int(char))
                else:
                    board_row.append(char)
            board.append(board_row)

        color_turn = split_fen[1]
        castling_rights = split_fen[2]
        en_passant = split_fen[3]
        half_move_count = int(split_fen[4])
        full_move_count = int(split_fen[5])

        return BoardRepresentation(
            board,
            color_turn,
            castling_rights,
            en_passant,
            half_move_count,
            full_move_count)

    def verify(self) -> None:
        """
        Verifies the FEN string.

        :return: None if all checks passed, raise an error otherwise
        """

        self._check_fen_structure()
        split_fen = self.fen.split(' ')

        self._check_first_field(split_fen[0])
        self._check_second_field(split_fen[1])
        self._check_third_field(split_fen[2])
        self._check_fourth_field(split_fen[3])
        self._check_fifth_field(split_fen[4])
        self._check_sixth_field(split_fen[5])

        self.verified = True

    def _check_fen_structure(self) -> None:
        """
        Checks the number of fields in the FEN string. A correct FEN must have 6 fields separated by a white space.

        :return: None if the number of fields is correct, raise an error otherwise.
        """
        split_fen = self.fen.split(" ")
        if len(split_fen) != 6:
            raise ValueError(f"Invalid FEN: Incorrect number of fields. Expected 6, got {len(split_fen)}.")

    def _check_first_field(self, first_field: str) -> None:
        """
        Checks the first field of the FEN string. The first field must contain 8 ranks separated by a "/" character.

        :return: None if the first field is correct, raise an error otherwise.
        """
        ranks = first_field.split("/")
        if len(ranks) != 8:
            raise ValueError(f"Invalid FEN: Incorrect number of ranks. Expected 8, got {len(ranks)}. Field: {first_field}")
        correct_characters = "rnbqkpRNBQKP12345678/"
        for char in first_field:
            if char not in correct_characters:
                raise ValueError(f"Invalid FEN: Incorrect characters in rank. Expected characters from {correct_characters}, got {char}")


    def _check_second_field(self, second_field: str) -> None:
        """
        Checks the second field of the FEN string. The second field must be either "w" or "b".

        :return: None if the second field is correct, raise an error otherwise.
        """
        if second_field not in ["w", "b"]:
            raise ValueError(f"Invalid FEN: Incorrect active color. Expected 'w' or 'b', got {second_field}")

    def _check_third_field(self, third_field) -> None:
        """
        Checks the third field of the FEN string. The third field must be a valid castling rights string.

        :return: None if the third field is correct, raise an error otherwise.
        """
        valid_castling_rights = ["K", "Q", "k", "q", "-"]
        if len(third_field) > 4:
            raise ValueError(f"Invalid FEN: Incorrect castling rights. Expected rights of the form 'KQkq' or '-', got {third_field}")
        if len(set(third_field)) != len(third_field):
            raise ValueError(f"Invalid FEN: Incorrect castling rights. Castling rights must be unique, got {third_field}")
        for char in third_field:
            if char not in valid_castling_rights:
                raise ValueError(f"Invalid FEN: Incorrect castling rights. Expected rights of the form 'KQkq' or '-', got {third_field}")
        if "-" in third_field and third_field != "-":
            raise ValueError(f"Invalid FEN: Incorrect castling rights. Expected rights of the form 'KQkq' or '-', got {third_field}")

    def _check_fourth_field(self, fourth_field) -> None:
        """
        Checks the fourth field of the FEN string. The fourth field must be a valid en passant target square.

        :return: None if the fourth field is correct, raise an error otherwise.
        """
        if fourth_field == "-":
            return
        if len(fourth_field) != 2:
            raise ValueError(f"Invalid FEN: Incorrect en passant target square. Expected a field of size 2, got {len(fourth_field)}: {fourth_field}")
        if fourth_field[0] not in 'abcdefgh' or fourth_field[1] not in '12345678':
            raise ValueError(f"Invalid FEN: Incorrect en passant target square. Must be a correct square, got {fourth_field}")

    def _check_fifth_field(self, fifth_field) -> None:
        """
        Checks the fifth field of the FEN string. The fifth field must be a valid halfmove clock.

        :return: None if the fifth field is correct, raise an error otherwise.
        """
        if not fifth_field.isdigit() or int(fifth_field) < 0:
            raise ValueError(f"Invalid FEN: Incorrect half-move clock. Expected a digit superior or equal to 0, got {fifth_field}")

    def _check_sixth_field(self, sixth_field) -> None:
        """
        Checks the sixth field of the FEN string. The sixth field must be a valid fullmove number.

        :return: None if the sixth field is correct, raise an error otherwise.
        """
        if not sixth_field.isdigit() or int(sixth_field) < 1:
            raise ValueError(f"Invalid FEN: Incorrect full-move number. Expected a digit superior to 0, got {sixth_field}")