from pieces.Rook import Rook
from pieces.Bishop import Bishop


class Queen(Rook, Bishop):
    pass


#    def __init__(self, color: str, initial_position: tuple, img_filename: str='') -> None:
#        super().__init__(color, initial_position, img_filename)
#
#
#    def find_legal_moves(self, player_1: object, player_2: object, color_to_move: str) -> list:
#        return super().find_legal_moves(player_1, player_2, color_to_move)

