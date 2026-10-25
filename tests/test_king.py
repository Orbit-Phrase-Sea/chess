from collections import Counter


import pytest


from player import Player
from pieces import King


@pytest.mark.parametrize('color', ['w', 'b'])
def test_king_init(color):
    player = Player(color, piece_setup='king')
    piece_name = type(player.get_king()).__name__
    selection_state =  player.get_king().is_selected()
    rank = 0 if color == 'b' else 7
    position = player.get_king().get_position()
    assert (piece_name, selection_state, position) == ('King', False, (4, rank))


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_edge_king_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='empty'),
            'b': Player('b', piece_setup='empty')
            }
    players['w'].set_king(King('w', (0, 7)))
    players['b'].set_king(King('b', (7, 7)))
    moves = [(0, 6), (1, 7), (1, 6)] if color_to_move == 'w' else [(6, 7), (7, 6), (6, 6)]
    assert Counter(players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)) == Counter(moves)

@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_middle_king_moves(color_to_move):
    players = {
            'w': Player('w', piece_setup='empty'),
            'b': Player('b', piece_setup='empty')
            }
    players['w'].set_king(King('w', (1, 4)))
    players['b'].set_king(King('b', (4, 2)))
    w_moves = [(0, 4), (0, 3), (0, 5), (1, 5), (1, 3), (2, 3), (2, 4), (2, 5)]
    b_moves = [(3, 1), (3, 2), (3, 3), (4, 3), (4, 1), (5, 1), (5, 2), (5, 3)]
    assert Counter(players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)) == Counter(w_moves if color_to_move=='w' else b_moves)

