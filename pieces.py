from player import Player


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


    def move(self, player_1: Player, player_2: Player, position: tuple) -> int:

        if not self.is_selected() or position not in self.find_legal_moves(player_1, player_2, self.color):
            return 1

        self.set_position(position)
        self._has_moved = True
        return 0


    def find_legal_moves(self, player_1: Player, player_2: Player, color_to_move: str) -> list:

        if color_to_move != 'b' and color_to_move != 'w':
            raise ValueError('color_to_move must be "w" or "b"')

        return []


    def check_for_checks(self, *, ally: Player, opponent: Player, position: tuple, color_to_move: str) -> bool:

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


    def _filter_for_checks(self, *, ally: Player, opponent: Player, color_to_move: str, moves: list) -> list:
        for pos in moves[::-1]:
            if self.check_for_checks(ally=ally, opponent=opponent, position=pos, color_to_move=color_to_move):
                moves.pop(moves.index(pos))

        return moves


    def ally_opponent(self, player_1: Player, player_2: Player) -> tuple:
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


class King(Piece):


    def find_legal_moves(self, player_1, player_2, color_to_move):
        legal_moves = super().find_legal_moves(player_1, player_2, color_to_move)
        ally, opponent = self.ally_opponent(player_1, player_2)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue

                move = (self.position[0] + i, self.position[1] + j)

                if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
                    continue

                legal_moves.append(move)

        ally_piece_pos = [piece.get_position() for piece in ally.get_piece_objects()]

        for pos in ally_piece_pos:
            if pos in legal_moves:
                legal_moves.pop(legal_moves.index(pos))

        if color_to_move == self.color:
            if self.castles_legality_check(ally=ally, opponent=opponent, side='k'):
                legal_moves.append((self.position[0]+2, self.position[1]))
            if self.castles_legality_check(ally=ally, opponent=opponent, side='q'):
                legal_moves.append((self.position[0]-2, self.position[1]))

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)


    def castles_legality_check(self, *, ally, opponent, side: str):
        if side not in ['k', 'q']:
            raise ValueError("side must be 'k' or 'q'")

        if self.has_moved():
            return False

        rank = 0 if self.color == 'b' else 7
        rook_check_passed = False
        if side == 'k':
            king_path = [(5, rank), (6, rank)]
            empty_positions = king_path
            rook_x = 7
        else:
            king_path = [(3, rank), (2, rank)]
            empty_positions = king_path + [(1, rank)]
            rook_x = 0

        for piece in ally.get_piece_objects()+opponent.get_piece_objects():
            if piece.get_position() in empty_positions:
                return False
            if piece.color == self.color and type(piece).__name__ == 'Rook' and piece.get_position() == (rook_x, rank):
                if not piece.has_moved():
                    rook_check_passed = True

        if not rook_check_passed:
            return False

        for piece in opponent.get_piece_objects():
            attacked_squares = piece.find_legal_moves(ally, opponent, self.color)
            for position in king_path:
                if position in attacked_squares:
                    return False

        return True


class Bishop(Piece):


    def find_legal_moves(self, player_1: Player, player_2: Player, color_to_move: str) -> list:
        legal_moves = super().find_legal_moves(player_1, player_2, color_to_move)
        ally, opponent = self.ally_opponent(player_1, player_2)

        ally_piece_pos = [piece.get_position() for piece in ally.get_piece_objects()]
        opponent_piece_pos = [piece.get_position() for piece in opponent.get_piece_objects()]

        ranges_of_interest = [
                (range(self.position[0]+1, 8), range(self.position[1]+1, 8)),
                (range(self.position[0]+1, 8), range(self.position[1]-1, -1, -1)),
                (range(self.position[0]-1, -1, -1), range(self.position[1]+1, 8)),
                (range(self.position[0]-1, -1, -1), range(self.position[1]-1, -1, -1)),
                ]

        for range_i, range_j in ranges_of_interest:
            for i, j in zip(range_i, range_j):
                move = i, j
                if not 0 <= move[0] < 8 or not 0 <= move[1] < 8:
                    break
    
                if move in ally_piece_pos:
                    break
    
                if move in opponent_piece_pos:
                    legal_moves.append(move)
                    break
    
                legal_moves.append(move)

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)


class Rook(Piece):


    def find_legal_moves(self, player_1: Player, player_2: Player, color_to_move: str) -> list:
        legal_moves = super().find_legal_moves(player_1, player_2, color_to_move)
        ally, opponent = self.ally_opponent(player_1, player_2)

        x_ally_intersects, y_ally_intersects  = [], []
        for piece in ally.get_piece_objects():
            if piece is self:
                continue

            pos = piece.get_position()
            if pos[0] == self.position[0]:
                y_ally_intersects.append(pos[1])
            elif pos[1] == self.position[1]:
                x_ally_intersects.append(pos[0])


        x_opponent_interects, y_opponent_interects = [], []
        for piece in opponent.get_piece_objects():
            pos = piece.get_position()
            if pos[0] == self.position[0]:
                y_opponent_interects.append(pos[1])
            elif pos[1] == self.position[1]:
                x_opponent_interects.append(pos[0])

        x_ally_intersects, y_ally_intersects  = sorted(x_ally_intersects), sorted(y_ally_intersects)
        x_opponent_interects, y_opponent_interects = sorted(x_opponent_interects), sorted(y_opponent_interects)
        min_x, max_x = 0, 7
        min_y, max_y = 0, 7
        for i in x_ally_intersects:
            if i < self.position[0]:
                min_x = i + 1
                continue
            max_x = i - 1
            break

        for i in y_ally_intersects:
            if i < self.position[1]:
                min_y = i + 1
                continue
            max_y = i - 1
            break

        for i in y_opponent_interects:
            if i < min_y or i > max_y:
                continue
            if i < self.position[1]:
                min_y = i
                continue
            max_y = i

        for i in x_opponent_interects:
            if i < min_x or i > max_x:
                continue
            if i < self.position[0]:
                min_x = i
                continue
            max_x = i


        for i in range(min_x, max_x+1):
            if i == self.position[0]:
                continue
            legal_moves.append((i, self.position[1]))

        for i in range(min_y, max_y+1):
            if i == self.position[1]:
                continue
            legal_moves.append((self.position[0], i))

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)


class Knite(Piece):


    def find_legal_moves(self, player_1: Player, player_2: Player, color_to_move: str) -> list:
        legal_moves = super().find_legal_moves(player_1, player_2, color_to_move)
        ally, opponent = self.ally_opponent(player_1, player_2)
        ally_piece_pos = [piece.get_position() for piece in ally.get_piece_objects()]

        for i, j in zip((-2, -2, -1, -1, 1, 1, 2, 2), (1, -1, 2, -2, 2, -2, 1, -1)):
            move = self.position[0] + i, self.position[1] + j
            if not 0 <= move[0] < 8 or not 0 <= move[1] < 8 or move in ally_piece_pos:
                continue

            legal_moves.append(move)

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)


class Pawn(Piece):


    def __init__(self, color: str, initial_position: tuple, img_filename: str='') -> None:
        super().__init__(color, initial_position, img_filename)
        self.has_moved_only_once = False


    def find_legal_moves(self, player_1, player_2, color_to_move):
        legal_moves = super().find_legal_moves(player_1, player_2, color_to_move)
        ally, opponent = self.ally_opponent(player_1, player_2)

        ally_piece_pos = [piece.get_position() for piece in ally.get_piece_objects()]
        opponent_piece_pos = [piece.get_position() for piece in opponent.get_piece_objects()]

        direction = 1 if self.color == 'b' else -1

        en_passant_capturable = opponent.get_en_passant_capturable()
        if (en_passant_capturable is not None
                and en_passant_capturable.get_position()[1] == self.position[1]
                and abs(en_passant_capturable.get_position()[0]-self.position[0]) == 1):
            legal_moves.append((en_passant_capturable.get_position()[0], self.position[1]+direction))

        # Check forward moves
        possible_moves = [
                (self.position[0], self.position[1]+direction*1),
                (self.position[0], self.position[1]+direction*2),
                ]
        if possible_moves[0] not in ally_piece_pos + opponent_piece_pos:
            legal_moves.append(possible_moves[0])
            if not self.has_moved() and possible_moves[1] not in ally_piece_pos + opponent_piece_pos:
                legal_moves.append(possible_moves[1])

        # Check capture moves (not en-passant)
        possible_moves = [
                (self.position[0]+1, self.position[1]+direction*1),
                (self.position[0]-1, self.position[1]+direction*1)
                ]
        for move in possible_moves:
            if not -1 < move[0] < 8 or not -1 < move[1] < 8:
                continue

            if move in opponent_piece_pos:
                legal_moves.append(move)

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)


    def move(self, player_1, player_2, position):
        if super().move(player_1, player_2, position):
            return 1

        if not self.has_moved():
            self.has_moved_only_once = True

        self.has_moved_only_once = False
        return 0


class Queen(Rook, Bishop):


    pass

