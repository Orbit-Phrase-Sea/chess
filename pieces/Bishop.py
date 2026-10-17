from pieces.Piece import Piece


class Bishop(Piece):


    def find_legal_moves(self, player_1: object, player_2: object, color_to_move: str) -> list:
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

