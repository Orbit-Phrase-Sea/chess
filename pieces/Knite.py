from pieces.Piece import Piece


class Knite(Piece):


    def find_legal_moves(self, player_1: object, player_2: object, color_to_move: str) -> list:
        legal_moves = super().find_legal_moves(player_1, player_2, color_to_move)
        ally, opponent = self.ally_opponent(player_1, player_2)
        ally_piece_pos = [piece.get_position() for piece in ally.get_piece_objects()]

        for i, j in zip((-2, -2, -1, -1, 1, 1, 2, 2), (1, -1, 2, -2, 2, -2, 1, -1)):
            move = self.position[0] + i, self.position[1] + j
            if not 0 <= move[0] < 8 or not 0 <= move[1] < 8 or move in ally_piece_pos:
                continue

            legal_moves.append(move)

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)

