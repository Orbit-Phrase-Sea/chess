from collections import Counter


import pytest


from player import Player
from pieces import Rook
import player


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_rook_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    players[color_to_move].add_piece(Rook(color_to_move, (3, 3)))
    expected_moves = []
    for i in range(8):
        if i == 3:
            continue
        expected_moves += [(i, 3), (3, i)]
    assert Counter(players[color_to_move].get_piece_objects()[-1].find_legal_moves(players['w'], players['b'], color_to_move)) == Counter(expected_moves)

