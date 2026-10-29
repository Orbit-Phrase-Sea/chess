from collections import Counter


from player import Player


def test_checkmate_1():
    players = {
            'w': Player('w', piece_setup='default'),
            'b': Player('b', piece_setup='default')
            }

    # 1. e4 ...
    players['w'].check_for_piece_selection((4, 6))
    players['w'].move_selected_piece(players['b'], (4, 4))

    # 1. e4 g5
    players['b'].check_for_piece_selection((6, 1))
    players['b'].move_selected_piece(players['w'], (6, 3))

    # 2. d4 ...
    players['w'].check_for_piece_selection((3, 6))
    players['w'].move_selected_piece(players['b'], (3, 4))

    # 2. d4 f6
    players['b'].check_for_piece_selection((5, 1))
    players['b'].move_selected_piece(players['w'], (5, 2))

    # 3. Qh5#
    players['w'].check_for_piece_selection((3, 7))
    players['w'].move_selected_piece(players['b'], (7, 3))

    black_has_no_moves = True
    for piece in players['b'].get_piece_objects():
        if piece.find_legal_moves(players['w'], players['b'], 'b'):
            black_has_no_moves = False
            break

    black_in_check = False
    b_king_pos = players['b'].get_king().get_position()
    for piece in players['w'].get_piece_objects():
        if b_king_pos in piece.find_legal_moves(players['b'], players['w'], 'b'):
            black_in_check = True
            break

    assert (black_has_no_moves, black_in_check) == (True, True)

