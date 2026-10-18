from pieces.Piece import Piece


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
        self.en_passant_capturable = None
        return 0

