from collections import Counter


import pytest


from player import Player
from pieces import Queen


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_queen_basic_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    queen_pos = (5, 3)
    queen = Queen(color_to_move, queen_pos)
    players[color_to_move].add_piece(queen, players['b' if color_to_move == 'w' else 'w'])

    expected_moves = []
    # Find rook moves
    for i in range(8):
        if i != queen_pos[0]:
            expected_moves.append((i, queen_pos[1]))
        if i != queen_pos[1]:
            expected_moves.append((queen_pos[0], i))

    # Find bishop moves
    for i in range(6):
        if i+2 != queen_pos[0]:
            expected_moves.append((i+2, i))

    for i in range(7):
        if i+1 != queen_pos[0]:
            expected_moves.append((i+1, 7-i))

    moves = queen.find_legal_moves(players['b'], players['w'], color_to_move)
    assert Counter(moves) == Counter(expected_moves)

