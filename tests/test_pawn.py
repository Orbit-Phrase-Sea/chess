from collections import Counter


import pytest


from player import Player
from pieces import Pawn


@pytest.mark.parametrize('pawn_x', [0, 2, 4, 7])
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_first_moves(color_to_move, pawn_x):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 1 if color_to_move == 'b' else 6
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players['b' if color_to_move == 'w' else 'w'])

    expected_moves = [(pawn_x, rank+1), (pawn_x, rank+2)]
    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

