from collections import Counter


import pytest


from pieces import Rook, Bishop


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('side', ['queen', 'king', 'both'])
def test_castles_empty_board(players_setup, color_to_move, side):
    players, opponent_color = players_setup('king', color_to_move)
    opponent_color = 'w' if color_to_move == 'b' else 'b'
    rank = 0 if color_to_move == 'b' else 7
    if side == 'queen':
        players[color_to_move].add_piece(Rook(color_to_move, (0, rank)), players[opponent_color])
    elif side == 'king':
        players[color_to_move].add_piece(Rook(color_to_move, (7, rank)), players[opponent_color])
    else:
        players[color_to_move].add_piece(Rook(color_to_move, (0, rank)), players[opponent_color])
        players[color_to_move].add_piece(Rook(color_to_move, (7, rank)), players[opponent_color])

    king_moves = players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)

    if side == 'queen':
        assert (2, rank) in king_moves and (6, rank) not in king_moves
    elif side == 'king':
        assert (6, rank) in king_moves and (2, rank) not in king_moves
    else:
        assert (2, rank) in king_moves and (6, rank) in king_moves


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_in_check(players_setup, color_to_move):
    players, opponent_color = players_setup('king', color_to_move)
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
def test_castles_attacked_path(players_setup, color_to_move, attacked_side):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 0 if color_to_move == 'b' else 7
    direction = 1 if color_to_move == 'b' else -1

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
        expected_moves = [(4, rank+direction)]

    expected_moves += [(3, rank+direction), (5, rank+direction)]

    moves = players[color_to_move].get_king().find_legal_moves(players['w'], players['b'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('blocking_color', ['w', 'b'])
@pytest.mark.parametrize('blocked_side', ['king', 'queen', 'both'])
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_blocked(players_setup, color_to_move, blocked_side, blocking_color):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 0 if color_to_move == 'b' else 7
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
def test_position_after_castles(players_setup, color_to_move, side):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 0 if color_to_move == 'b' else 7

    k_rook = Rook(color_to_move, (7, rank))
    q_rook = Rook(color_to_move, (0, rank))
    players[color_to_move].add_piece(q_rook, players[opponent_color])
    players[color_to_move].add_piece(k_rook, players[opponent_color])

    players[color_to_move].check_for_piece_selection((4, rank))
    expected_king_position = (2 if side == 'queen' else 6, rank)
    players[color_to_move].move_selected_piece(players[opponent_color], expected_king_position)

    expected_k_rook_position = (7 if side == 'queen' else 5, rank)
    expected_q_rook_position = (3 if side == 'queen' else 0, rank)

    assert expected_king_position == players[color_to_move].get_king().get_position()
    assert expected_q_rook_position == q_rook.get_position()
    assert expected_k_rook_position == k_rook.get_position()


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_castles_with_moved_king(players_setup, color_to_move):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 0 if color_to_move == 'b' else 7

    k_rook = Rook(color_to_move, (7, rank))
    q_rook = Rook(color_to_move, (0, rank))
    players[color_to_move].add_piece(q_rook, players[opponent_color])
    players[color_to_move].add_piece(k_rook, players[opponent_color])

    players[color_to_move].check_for_piece_selection((4, rank))
    players[color_to_move].move_selected_piece(players[opponent_color], (3, rank))
    players[color_to_move].check_for_piece_selection((3, rank))
    players[color_to_move].move_selected_piece(players[opponent_color], (4, rank))

    direction = 1 if color_to_move == 'b' else -1
    expected_moves = [(3, rank), (5, rank)] + [(i, rank+direction) for i in range(3, 6)]
    moves = players[color_to_move].get_king().find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('color_to_move', ['w', 'b'])
@pytest.mark.parametrize('rook_to_move', ['q_rook', 'k_rook'])
def test_castles_with_moved_rook(players_setup, color_to_move, rook_to_move):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 0 if color_to_move == 'b' else 7

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

    direction = 1 if color_to_move == 'b' else -1
    expected_moves = [(3, rank), (5, rank)] + [(i, rank+direction) for i in range(3, 6)]
    expected_moves.append((2 if rook_to_move == 'k_rook' else 6, rank))
    moves = players[color_to_move].get_king().find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)

