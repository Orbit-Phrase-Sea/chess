from collections import Counter


import pytest


from player import Player
from pieces import Rook, Knight


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_knight_edge_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    players[color_to_move].add_piece(Knight(color_to_move, (0, 0)), players[opponent_color])
    expected_moves = [(1, 2), (2, 1)]
    assert Counter(players[color_to_move].get_piece_objects()[-1].find_legal_moves(players['w'], players['b'], color_to_move)) == Counter(expected_moves)



@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('blocking_piece_color', ['w', 'b'])
def test_knight_with_piece(color_to_move, blocking_piece_color):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    players[color_to_move].add_piece(Knight(color_to_move, (3, 3)), players[opponent_color])
    players[blocking_piece_color].add_piece(Rook(blocking_piece_color, (2, 5)), players[opponent_color])

    expected_moves = [(2, 1), (1, 2), (1, 4), (4, 5), (5, 4), (5, 2), (4, 1)]
    if blocking_piece_color != color_to_move:
        expected_moves.append((2, 5))

    moves = players[color_to_move].get_piece_objects()[1].find_legal_moves(players['w'], players['b'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

