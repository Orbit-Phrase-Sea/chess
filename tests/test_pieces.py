import pytest


from player import Player
from pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn, Position


@pytest.mark.parametrize('color', ['w', 'b'])
def test_king_init(color):
    player = Player(color, piece_setup='king')
    piece_name = type(player.get_king()).__name__
    selection_state =  player.get_king().is_selected()
    rank = 0 if color == 'b' else 7
    position = player.get_king().get_position()
    assert (piece_name, selection_state, position) == ('King', False, (4, rank))

