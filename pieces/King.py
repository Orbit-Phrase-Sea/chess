from pieces.Piece import Piece


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

        return self._filter_for_checks(ally=ally, opponent=opponent, color_to_move=color_to_move, moves=legal_moves)


    def king_side_castles_legality_check(self, *, ally, opponent):
        if self.has_moved():
            return False

        rank = 0 if self.color == 'b' else 7
        rook_check_passed = False
        critical_positions = [self.get_position(), (5, rank), (6, rank)]
        for piece in ally.get_piece_objects()+opponent.get_piece_objects():
            if piece.get_position() in critical_positions[1:]:
                return False
            if piece.color == self.color and type(piece).__name__ == 'Rook' and piece.get_position() == (7, rank):
                if not piece.has_moved():
                    rook_check_passed = True

        if not rook_check_passed:
            return False

        for piece in opponent.get_piece_objects():
            attacked_squares = piece.find_legal_moves(ally, opponent, self.color)
            for position in critical_positions:
                if position in attacked_squares:
                    return False

        return True

