from pieces.Piece import Piece


class Rook(Piece):


    def find_legal_moves(self, player_1: object, player_2: object, color_to_move: str) -> list:
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

