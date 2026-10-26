from typing import Counter
import pytest


from player import Player
from pieces import Rook, Bishop


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('side', ['queen', 'king', 'both'])
def test_castles_empty_board(color_to_move, side):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    rank = 0 if color_to_move == 'b' else 7
    players[color_to_move].add_piece(Rook(color_to_move, (0, rank)), players[opponent_color])
    players[color_to_move].add_piece(Rook(color_to_move, (7, rank)), players[opponent_color])
    king_moves = players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)

    if side == 'queen':
        assert (2, rank) in king_moves
    if side == 'king':
        assert (6, rank) in king_moves
    assert (2, rank) in king_moves and (6, rank) in king_moves


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_in_check(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    rank = 0 if color_to_move == 'b' else 7
    bishop = Bishop(opponent_color, (1, 4 if color_to_move == 'w' else 3))

    players[opponent_color].add_piece(bishop, players[color_to_move])
    players[color_to_move].add_piece(Rook(color_to_move, (0, rank)), players[opponent_color])
    players[color_to_move].add_piece(Rook(color_to_move, (7, rank)), players[opponent_color])

    expected_moves = [(3, rank), (5, rank)]
    if color_to_move == 'w':
        expected_moves += [(4, rank-1), (5, rank-1)]
    else:
        expected_moves += [(4, rank+1), (5, rank+1)]

    moves = players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

