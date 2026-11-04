def test_checkmate_1(players_setup):
    players, _ = players_setup('default')

    # e4 g5, d4 f6, Qh5#
    for color, m_from, m_to in [
            ['w', (4, 6), (4, 4)], # e4
            ['b', (6, 1), (6, 3)], # g5
            ['w', (3, 6), (3, 4)], # d4
            ['b', (5, 1), (5, 2)], # f6
            ['w', (3, 7), (7, 3)], # Qh5#
            ]:
        players[color].check_for_piece_selection(m_from)
        players[color].move_selected_piece(players['b' if color == 'w' else 'w'], m_to)

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

    assert black_has_no_moves
    assert black_in_check

