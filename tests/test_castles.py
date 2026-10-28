from typing import Counter
import pytest


from player import Player
from pieces import King, Rook, Bishop


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


@pytest.mark.parametrize('attacked_side', ['queen', 'king', 'both'])
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_attacked_path(color_to_move, attacked_side):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king'),
            }
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    rank = 0 if color_to_move == 'b' else 7
    diraction = 1 if color_to_move == 'b' else -1

    if attacked_side == 'king':
        bishop = Bishop(opponent_color, (2, 4 if color_to_move == 'w' else 3))
    elif attacked_side == 'queen':
        bishop = Bishop(opponent_color, (6, 4 if color_to_move == 'w' else 3))
    else:
        bishop = Bishop(opponent_color, (4, 6 if color_to_move == 'w' else 1))

    players[opponent_color].add_piece(bishop, players[color_to_move])
    players[color_to_move].add_piece(Rook(color_to_move, (0, rank)), players[opponent_color])
    players[color_to_move].add_piece(Rook(color_to_move, (7, rank)), players[opponent_color])

    if attacked_side == 'queen':
        expected_moves = [(6, rank), (5, rank)]
    elif attacked_side == 'king':
        expected_moves = [(2, rank), (3, rank)]
    else:
        expected_moves = [(4, rank+diraction)]

    expected_moves += [(3, rank+diraction), (5, rank+diraction)]

    moves = players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('blocking_color', ['w', 'b'])
@pytest.mark.parametrize('blocked_side', ['king', 'queen', 'both'])
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_blocked(color_to_move, blocked_side, blocking_color):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 0 if color_to_move == 'b' else 7
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    blocking_color_opponent = 'w' if blocking_color == 'b' else 'b'

    if blocked_side == 'queen':
        players[blocking_color].add_piece(Bishop(blocking_color, (3, rank)), players[blocking_color_opponent])
    elif blocked_side == 'king':
        players[blocking_color].add_piece(Bishop(blocking_color, (5, rank)), players[blocking_color_opponent])
    else:
        players[blocking_color].add_piece(Bishop(blocking_color, (5, rank)), players[blocking_color_opponent])
        players[blocking_color].add_piece(Bishop(blocking_color, (3, rank)), players[blocking_color_opponent])

    players[color_to_move].add_piece(Rook(color_to_move, (0, rank)), players[opponent_color])
    players[color_to_move].add_piece(Rook(color_to_move, (7, rank)), players[opponent_color])

    moves = players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)

    if blocked_side == 'queen':
        assert (6, rank) in moves and (2, rank) not in moves
    elif blocked_side == 'king':
        assert (2, rank) in moves and (6, rank) not in moves
    else:
        assert (6, rank) not in moves and (2, rank) not in moves


@pytest.mark.parametrize('side', ['king', 'queen'])
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_position_after_castles(color_to_move, side):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 0 if color_to_move == 'b' else 7
    opponent_color = 'w' if color_to_move == 'b' else 'b'

    k_rook = Rook(color_to_move, (7, rank))
    q_rook = Rook(color_to_move, (0, rank))
    players[color_to_move].add_piece(q_rook, players[opponent_color])
    players[color_to_move].add_piece(k_rook, players[opponent_color])

    players[color_to_move].check_for_piece_selection((4, rank))
    expected_king_position = (2 if side == 'queen' else 6, rank)
    players[color_to_move].move_selected_piece(players[opponent_color], expected_king_position)

    expected_k_rook_position = (7 if side == 'queen' else 5, rank)
    expected_q_rook_position = (3 if side == 'queen' else 0, rank)

    assert (expected_king_position, expected_q_rook_position, expected_k_rook_position)\
            == (players[color_to_move].get_king().get_position(), q_rook.get_position(), k_rook.get_position())


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_with_moved_king(color_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 0 if color_to_move == 'b' else 7
    opponent_color = 'w' if color_to_move == 'b' else 'b'

    k_rook = Rook(color_to_move, (7, rank))
    q_rook = Rook(color_to_move, (0, rank))
    players[color_to_move].add_piece(q_rook, players[opponent_color])
    players[color_to_move].add_piece(k_rook, players[opponent_color])

    players[color_to_move].check_for_piece_selection((4, rank))
    players[color_to_move].move_selected_piece(players[opponent_color], (3, rank))
    players[color_to_move].check_for_piece_selection((3, rank))
    players[color_to_move].move_selected_piece(players[opponent_color], (4, rank))

    diraction = 1 if color_to_move == 'b' else -1
    expected_moves = [(3, rank), (5, rank)] + [(i, rank+diraction) for i in range(3, 6)]
    moves = players[color_to_move].get_king().find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('rook_to_move', ['q_rook', 'k_rook'])
def test_castles_with_moved_rook(color_to_move, rook_to_move):
    players = {
            'w': Player('w', piece_setup='king'),
            'b': Player('b', piece_setup='king')
            }
    rank = 0 if color_to_move == 'b' else 7
    opponent_color = 'w' if color_to_move == 'b' else 'b'

    k_rook = Rook(color_to_move, (7, rank))
    q_rook = Rook(color_to_move, (0, rank))
    players[color_to_move].add_piece(q_rook, players[opponent_color])
    players[color_to_move].add_piece(k_rook, players[opponent_color])

    rook_x_move = 1 if rook_to_move == 'q_rook' else 6
    rook = k_rook if rook_to_move == 'k_rook' else q_rook
    players[color_to_move].check_for_piece_selection(rook.get_position())
    players[color_to_move].move_selected_piece(players[opponent_color], (rook_x_move, rank))
    players[color_to_move].check_for_piece_selection((rook_x_move, rank))
    players[color_to_move].move_selected_piece(players[opponent_color], (0 if rook_to_move == 'q_rook' else 7, rank))

    diraction = 1 if color_to_move == 'b' else -1
    expected_moves = [(3, rank), (5, rank)] + [(i, rank+diraction) for i in range(3, 6)]
    expected_moves.append((2 if rook_to_move == 'k_rook' else 6, rank))
    moves = players[color_to_move].get_king().find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

