from collections import Counter


import pytest


from player import Player
from pieces import Rook, Knight


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_rook_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    players[color_to_move].add_piece(Rook(color_to_move, (3, 3)), players[opponent_color])
    expected_moves = []
    for i in range(8):
        if i == 3:
            continue
        expected_moves += [(i, 3), (3, i)]
    assert Counter(players[color_to_move].get_piece_objects()[-1].find_legal_moves(players['w'], players['b'], color_to_move)) == Counter(expected_moves)



@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('blocking_piece_color', ['w', 'b'])
def test_rook_with_piece(color_to_move, blocking_piece_color):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    players[color_to_move].add_piece(Rook(color_to_move, (3, 3)), players[opponent_color])
    players[blocking_piece_color].add_piece(Knight(blocking_piece_color, (3, 1)), players[opponent_color])

    expected_moves = []
    for i in range(8):
        if i == 3:
            continue
        expected_moves.append((i, 3))
        if i < 2:
            continue
        expected_moves.append((3, i))

    if blocking_piece_color != color_to_move:
        expected_moves.append((3, 1))

    moves = players[color_to_move].get_piece_objects()[1].find_legal_moves(players['w'], players['b'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

