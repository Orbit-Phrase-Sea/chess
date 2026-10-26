from collections import Counter


import pytest


from player import Player
from pieces import Bishop, Pawn


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_bishop_edge_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    players[color_to_move].add_piece(Bishop(color_to_move, (7, 0)), players[opponent_color])
    expected_moves = [(7-i, i) for i in range(1, 8)]
    assert Counter(players[color_to_move].get_piece_objects()[-1].find_legal_moves(players['w'], players['b'], color_to_move)) == Counter(expected_moves)



@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('blocking_piece_color', ['w', 'b'])
def test_bishop_with_piece(color_to_move, blocking_piece_color):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    players[color_to_move].add_piece(Bishop(color_to_move, (6, 4)), players[opponent_color])
    players[blocking_piece_color].add_piece(Pawn(blocking_piece_color, (5, 5)), players[opponent_color])

    expected_moves = [(7, 3)]
    for i in range(6):
        if i == 4:
            continue
        expected_moves.append((i+2, i))

    if blocking_piece_color != color_to_move:
        expected_moves.append((5, 5))

    moves = players[color_to_move].get_piece_objects()[1].find_legal_moves(players['w'], players['b'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

