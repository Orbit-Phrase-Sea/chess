from typing import Counter
import pytest


from player import Player
from pieces import Bishop, Pawn, Queen, Rook


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pin_1(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    rank = 1 if color_to_move == 'b' else 6
    pawn = Pawn(color_to_move, (5, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])
    players[opponent_color].add_piece(Bishop(opponent_color, (7, 4 if color_to_move=='w' else 3)), players[opponent_color])

    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert moves == []


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pin_2(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    rank = 2 if color_to_move == 'b' else 5
    queen = Queen(color_to_move, (4, rank))
    rook = Rook(opponent_color, (4, 4 if color_to_move == 'b' else 3))
    players[color_to_move].add_piece(queen, players[opponent_color])
    players[opponent_color].add_piece(rook, players[opponent_color])

    moves = queen.find_legal_moves(players['b'], players['w'], color_to_move)
    expected_moves = [(4, 3), (4, 4), (4, 1 if color_to_move == 'b' else 6)]

    assert Counter(moves) == Counter(expected_moves)

