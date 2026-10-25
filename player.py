from pieces import King, Queen, Rook, Bishop, Knight, Pawn, Piece, Position


class Player:

    def __init__(self, color: str, piece_setup: str='default') -> None:
        if piece_setup not in ['default', 'king', 'empty']:
            raise ValueError('piece_setup must be one of: "default", "empty"')

        self.color: str = color
        self.selected_piece = None
        self.en_passant_capturable = None
        self.king = None
        self.active_piece_list: list = []
        self.move_history: list = []
        rank = 0 if color == 'b' else 7

        if piece_setup == 'default' or piece_setup == 'king':
            self.king = King(color, initial_position=(4, rank), img_filename=color+'K.svg')
            self.active_piece_list.append(self.king)
        if piece_setup == 'default':
            self.active_piece_list += [
                                        Bishop(self.color, initial_position=(2, rank), img_filename=color+'B.svg'),
                                        Bishop(self.color, initial_position=(5, rank), img_filename=color+'B.svg'),
                                        Knight(self.color, initial_position=(1, rank), img_filename=color+'N.svg'),
                                        Knight(self.color, initial_position=(6, rank), img_filename=color+'N.svg'),
                                        Rook(color, initial_position=(0, rank), img_filename=color+'R.svg'),
                                        Rook(color, initial_position=(7, rank), img_filename=color+'R.svg'),
                                        Queen(color, initial_position=(3, rank), img_filename=color+'Q.svg'),
                                    ]
            self.active_piece_list += [Pawn(self.color, initial_position=(i, 6 if rank==7 else 1), img_filename=color+'P.svg') for i in range(8)]


    def check_for_piece_selection(self, position: Position) -> bool:
        """Returns True if a piece was selected and False otherwise"""

        for piece in self.get_piece_objects():
            if piece.get_position()[0] == position[0] and piece.get_position()[1] == position[1]:
                if piece is self.selected_piece:
                    self.selected_piece = None
                    piece.set_selected(False)
                    return False

                if not piece.is_selected() and self.has_selected_piece():
                    self.selected_piece.set_selected(False)
                    self.selected_piece = piece
                    self.selected_piece.set_selected(True)
                    return True

                piece.set_selected(True)
                self.selected_piece = piece
                return True

        return False


    def move_selected_piece(self, opponent: Player, position: Position) -> bool:
        if opponent.get_color() == self.color:
            raise ValueError("opponent.color cannot be the same as self.color")

        if self.selected_piece is None:
            return False

        move_log = str(self.selected_piece.get_position()[0]) + str(self.selected_piece.get_position()[1])

        moved = not self.selected_piece.move(self, opponent, position)
        self.selected_piece.set_selected(False)

        if not moved:
            self.selected_piece = None
            return False

        self.en_passant_capturable = None

        direction = 1 if self.color == 'b' else -1
        for piece_idx, piece in  enumerate(opponent.get_piece_objects()):
            if (piece.get_position() == self.selected_piece.get_position()):
                move_log += 'x'
                opponent.get_piece_objects().pop(piece_idx)

            # Captured en-passant
            elif type(self.selected_piece).__name__ == 'Pawn' == type(piece).__name__ == 'Pawn' and piece.get_position() == (position[0], position[1]-direction):
                move_log += 'x'
                opponent.get_piece_objects().pop(piece_idx)


        move_log += str(position[0]) + str(position[1])

        # Castles
        k_rook, q_rook = None, None
        if type(self.selected_piece).__name__ == 'King' and abs(position[0] - int(move_log[0])) == 2:
            for piece in self.active_piece_list:
                if type(piece).__name__ == 'Rook' and not piece.has_moved():
                    if piece.get_position()[0] == 0:
                        q_rook = piece
                    elif piece.get_position()[0] == 7:
                        k_rook = piece
        if self.selected_piece is self.king and position[0] - int(move_log[0]) == 2:
            k_rook.set_position((5, k_rook.get_position()[1]))
        if self.selected_piece is self.king and int(move_log[0]) - position[0] == 2:
            q_rook.set_position((3, q_rook.get_position()[1]))
        self.move_history.append(move_log)

        # Check whether opponent can capture the moved piece en-passant
        if type(self.selected_piece).__name__ == 'Pawn' and abs(int(move_log[1])-int(move_log[-1])) == 2:
            self.en_passant_capturable = self.selected_piece

        self.selected_piece = None
        return True


    def is_to_promote(self) -> bool:
        for piece in self.active_piece_list:
            if type(piece).__name__ != 'Pawn':
                continue
            if piece.get_position()[1] == (7 if self.color == 'b' else 0):
                return True

        return False


    def promote(self, code: int) -> Piece:
        for idx, piece in enumerate(self.active_piece_list):
            if type(piece).__name__ != 'Pawn':
                continue
            if piece.get_position()[1] == (7 if self.color == 'b' else 0):
                piece_idx = idx
                break
        # No break
        else:
            raise RuntimeError("Invalid promotion request.")

        pos = self.active_piece_list[piece_idx].get_position()
        self.active_piece_list.pop(piece_idx)

        options = [Queen, Rook, Knight, Bishop]
        piece_symbol = 'QRNB'

        self.active_piece_list.insert(piece_idx, options[code-1](self.color, pos, img_filename=self.color+piece_symbol[code-1]+'.svg'))
        return self.active_piece_list[piece_idx]


    def has_selected_piece(self) -> bool:
        return True if self.selected_piece else False


    def remove_selection(self) -> None:
        self.selected_piece = None


    def get_selected_piece(self):
        return self.selected_piece


    def add_piece(self, new_piece: Piece, opponent: Player) -> None:
        if isinstance(new_piece, King):
            raise ValueError("Use the set_king method to set the king instead")
        if new_piece.get_color() != self.color:
            raise ValueError("The color of the piece added must be the same color as the player")

        for piece in self.active_piece_list + opponent.get_piece_objects():
            if piece.get_position() == new_piece.get_position():
                raise ValueError(f"There is already a piece in position={new_piece.get_position()}")

        self.active_piece_list.append(new_piece)


    def set_king(self, king: King, opponent: Player) -> None:
        for piece in self.active_piece_list + opponent.get_piece_objects():
            if king.get_position() == piece.get_position():
                raise ValueError("There is already a piece in that position")

        if self.king is None:
            self.active_piece_list.append(king)
            self.king = king
            return

        for idx, piece in enumerate(self.active_piece_list):
            if isinstance(piece, King):
                self.active_piece_list[idx] = king
                break

        self.king = king


    def get_king(self):
        return self.king


    def get_piece_img_filenames(self) -> list:
        img_filenames = [piece.get_img_filename() for piece in self.active_piece_list]
        return img_filenames


    def get_piece_objects(self) -> list:
        return self.active_piece_list


    def set_en_passant_capturable(self, piece) -> None:
        self.en_passant_capturable = piece


    def get_en_passant_capturable(self):
        return self.en_passant_capturable


    def get_color(self) -> str:
        return self.color

