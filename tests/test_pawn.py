from collections import Counter


import pytest


from player import Player
from pieces import King, Pawn


@pytest.mark.parametrize('pawn_x', range(8))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_first_moves(color_to_move, pawn_x):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 1 if color_to_move == 'b' else 6
    diraction = -1 if color_to_move == 'w' else 1
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players['b' if color_to_move == 'w' else 'w'])

    expected_moves = [(pawn_x, rank+diraction), (pawn_x, rank+diraction*2)]
    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('forward_squares', [1, 2])
@pytest.mark.parametrize('pawn_x', range(8))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_second_moves(color_to_move, pawn_x, forward_squares):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 1 if color_to_move == 'b' else 6
    diraction = -1 if color_to_move == 'w' else 1
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])
    players[color_to_move].check_for_piece_selection((pawn_x, rank))
    players[color_to_move].move_selected_piece(players[opponent_color], (pawn_x, rank+diraction*forward_squares))

    expected_moves = [(pawn_x, rank+diraction*(1 + forward_squares))]
    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('promote_id', range(1, 5)) # 1: queen, 2: rook, 3: knight, 4: bishop
@pytest.mark.parametrize('pawn_x', range(8))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_promotion(color_to_move, pawn_x, promote_id):
    players = {
            'w': Player('w', piece_setup='empty'),
            'b': Player('b', piece_setup='empty')
            }
    players['w'].set_king(King('w', (5, 4)), players['b'])
    players['b'].set_king(King('b', (3, 4)), players['w'])
    rank = 7 if color_to_move == 'b' else 0
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])
    promotion_detected = players[color_to_move].is_to_promote()
    new_piece = players[color_to_move].promote(promote_id)

    options = ['Queen', 'Rook', 'Knight', 'Bishop']

    assert (promotion_detected, options[promote_id-1]) == (True, type(new_piece).__name__)

