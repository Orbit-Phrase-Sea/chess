class Piece:


    def __init__(self, color: str, initial_position: tuple, img_filename: str='') -> None:
        if color not in ['w', 'b']:
            raise ValueError('color must be "w" or "b"')
        self.color = color

        if len(initial_position) != 2:
            raise ValueError('initial_position must be a tuple of length 2')
        elif 0 < initial_position[0] >= 8 or 0 < initial_position[1] >= 8:
            raise ValueError('The elements of initial_position must be in [0, 7] exclusively')
        else:
            self.position = initial_position

        self.img_filename = img_filename
        self.selected = False
        self._has_moved = False


    def move(self, player_1: object, player_2: object, position: tuple) -> int:

        if not self.is_selected() or position not in self.find_legal_moves(player_1, player_2, self.color):
            return 1

        self.set_position(position)
        self._has_moved = True
        return 0


    def find_legal_moves(self, player_1: object, player_2: object, color_to_move: str) -> list:

        if color_to_move != 'b' and color_to_move != 'w':
            raise ValueError('color_to_move must be "w" or "b"')

        return []


    def check_for_checks(self, *, ally: object, opponent: object, position: tuple, color_to_move: str) -> bool:

        if self.color != color_to_move:
            return False

        position_bak = self.get_position()
        self.set_position(position)

        captured_piece, captured_idx = None, None
        for idx, piece in enumerate(opponent.get_piece_objects()):
            if self.position == piece.get_position():
                captured_idx, captured_piece = idx, opponent.get_piece_objects().pop(idx)

        king_position = ally.get_piece_objects()[0].get_position()
        for opponent_piece in opponent.get_piece_objects():

            if opponent_piece.get_position() == self.position:
                continue

            if king_position in opponent_piece.find_legal_moves(ally, opponent, color_to_move):
                self.set_position(position_bak)
                if captured_idx is not None:
                    opponent.get_piece_objects().insert(captured_idx, captured_piece)
                return True

        self.set_position(position_bak)
        if captured_idx is not None:
            opponent.get_piece_objects().insert(captured_idx, captured_piece)
        return False


    def _filter_for_checks(self, *, ally: object, opponent: object, color_to_move: str, moves: list) -> list:
        for pos in moves[::-1]:
            if self.check_for_checks(ally=ally, opponent=opponent, position=pos, color_to_move=color_to_move):
                moves.pop(moves.index(pos))

        return moves


    def ally_opponent(self, player_1: object, player_2: object) -> tuple:
        if player_1.color == self.color:
            return player_1, player_2
        return player_2, player_1


    def is_selected(self) -> bool:
        return self.selected


    def has_moved(self) -> bool:
        return self._has_moved


    def set_img(self, img_object: object) -> None:
        self.img = img_object


    def get_img_filename(self) -> str:
        return self.img_filename


    def get_img(self) -> object:
        return self.img


    def set_position(self, position: tuple) -> None:
        self.position = position


    def get_position(self) -> tuple:
        return self.position


    def set_selected(self, selected: bool) -> None:
        self.selected = selected

