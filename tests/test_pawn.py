from collections import Counter

import pytest

from pieces import King, Knight, Pawn, Queen, Bishop, Rook


@pytest.mark.parametrize('pawn_x', range(8))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_first_moves(players_setup, color_to_move, pawn_x):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 1 if color_to_move == 'b' else 6
    direction = -1 if color_to_move == 'w' else 1
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])

    expected_moves = [(pawn_x, rank+direction), (pawn_x, rank+direction*2)]
    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('pawn_x', range(1, 6))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_captures(players_setup, color_to_move, pawn_x):
    players, opponent_color = players_setup('king', color_to_move)
    direction = -1 if color_to_move == 'w' else 1
    rank = 4
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])
    players[color_to_move].add_piece(
        Knight(color_to_move, (pawn_x-1, rank+direction)),
        players[opponent_color],
    )
    players[opponent_color].add_piece(
        Knight(opponent_color, (pawn_x+1, rank+direction)),
        players[color_to_move],
    )
    players[opponent_color].add_piece(
        Knight(opponent_color, (pawn_x, rank+direction)),
        players[color_to_move],
    )

    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert moves == [(pawn_x+1, rank+direction)]


@pytest.mark.parametrize('forward_squares', [1, 2])
@pytest.mark.parametrize('pawn_x', range(8))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_second_moves(players_setup, color_to_move, pawn_x, forward_squares):
    players, opponent_color = players_setup('king', color_to_move)
    rank = 1 if color_to_move == 'b' else 6
    direction = -1 if color_to_move == 'w' else 1
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])
    players[color_to_move].check_for_piece_selection((pawn_x, rank))
    players[color_to_move].move_selected_piece(
        players[opponent_color],
        (pawn_x, rank+direction*forward_squares),
    )

    expected_moves = [(pawn_x, rank + direction * (1+forward_squares))]
    moves = pawn.find_legal_moves(players['b'], players['w'], color_to_move)

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('promote_id', range(1, 5)) # 1: queen, 2: rook, 3: knight, 4: bishop
@pytest.mark.parametrize('pawn_x', range(8))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_pawn_promotion(players_setup, color_to_move, pawn_x, promote_id):
    players, opponent_color = players_setup('empty', color_to_move)
    players['w'].set_king(King('w', (5, 4)), players['b'])
    players['b'].set_king(King('b', (3, 4)), players['w'])
    rank = 7 if color_to_move == 'b' else 0
    pawn = Pawn(color_to_move, (pawn_x, rank))
    players[color_to_move].add_piece(pawn, players[opponent_color])
    promotion_detected = players[color_to_move].is_to_promote()
    new_piece = players[color_to_move].promote(promote_id)

    expected_piece = [Queen, Rook, Knight, Bishop]
    expected_position = (pawn_x, rank)

    assert promotion_detected
    assert expected_piece[promote_id-1] is type(new_piece)
    assert expected_position == new_piece.get_position()


@pytest.mark.parametrize('pawn_x', range(1, 6))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_captures_en_passant(players_setup, color_to_move, pawn_x):
    players, opponent_color = players_setup('king', color_to_move)

    direction = -1 if color_to_move == 'w' else 1
    rank = 3 if color_to_move == 'b' else 4

    pawn = Pawn(color_to_move, (pawn_x, rank))
    opponent_pawn = Pawn(opponent_color, (pawn_x+1, rank+direction*3))

    players[color_to_move].add_piece(pawn, players[opponent_color])
    players[opponent_color].add_piece(opponent_pawn, players[color_to_move])

    players[opponent_color].check_for_piece_selection((pawn_x+1, rank+direction*3))
    players[opponent_color].move_selected_piece(
        players[color_to_move],
        (pawn_x+1, rank+direction*2),
    )

    players[color_to_move].check_for_piece_selection((pawn_x, rank))
    players[color_to_move].move_selected_piece(
        players[opponent_color],
        (pawn_x, rank+direction*2),
    )

    expected_moves = [(pawn_x, rank+direction), (pawn_x+1, rank+direction)]
    moves = opponent_pawn.find_legal_moves(
        players['b'],
        players['w'],
        opponent_pawn.get_color(),
    )

    assert Counter(moves) == Counter(expected_moves)


@pytest.mark.parametrize('pawn_x', range(1, 6))
@pytest.mark.parametrize('color_to_move', ['w', 'b'])
def test_captures_en_passant_not_next_move(players_setup, color_to_move, pawn_x):
    players, opponent_color = players_setup('king', color_to_move)

    direction = -1 if color_to_move == 'w' else 1
    rank = 3 if color_to_move == 'b' else 4

    pawn = Pawn(color_to_move, (pawn_x, rank))
    opponent_pawn = Pawn(opponent_color, (pawn_x+1, rank+direction*3))

    players[color_to_move].add_piece(pawn, players[opponent_color])
    players[opponent_color].add_piece(opponent_pawn, players[color_to_move])

    players[opponent_color].check_for_piece_selection((pawn_x+1, rank+direction*3))
    players[opponent_color].move_selected_piece(
        players[color_to_move],
        (pawn_x+1, rank+direction*2),
    )

    players[color_to_move].check_for_piece_selection((pawn_x, rank))
    players[color_to_move].move_selected_piece(
        players[opponent_color],
        (pawn_x, rank+direction*2),
    )

    opponent_rank = 0 if opponent_color == 'b' else 7
    players[opponent_color].check_for_piece_selection((4, opponent_rank))
    players[opponent_color].move_selected_piece(
        players[color_to_move],
        (5, opponent_rank),
    )

    players[color_to_move].check_for_piece_selection((4, rank-direction*3))
    players[color_to_move].move_selected_piece(
        players[opponent_color],
        (5, rank-direction*3),
    )

    expected_moves = [(pawn_x+1, rank+direction)]
    moves = opponent_pawn.find_legal_moves(
        players['b'],
        players['w'],
        opponent_pawn.get_color(),
    )

    assert moves == expected_moves


@pytest.mark.parametrize('enemy_pawn_x', range(1, 6))
@pytest.mark.parametrize('ally_color', ['w', 'b'])
def test_en_passant_creates_discovery(players_setup, ally_color, enemy_pawn_x):
    players, opponent_color = players_setup('king', ally_color)

    # ally_color will be attempting the illegal capture
    rank_of_interest = 3 if ally_color == 'w' else 4

    players[opponent_color].add_piece(
        Rook(opponent_color, (7, rank_of_interest)),
        players[ally_color],
    )

    enemy_pawn = Pawn(
        opponent_color,
        (enemy_pawn_x, 1 if ally_color == 'w' else 6),
    )
    bad_move = ( # This move should not be allowed
        enemy_pawn_x,
        2 if ally_color == 'w' else 5,
    )
    players[opponent_color].add_piece(
        enemy_pawn,
        players[ally_color],
    )

    ally_pawn = Pawn(ally_color, (enemy_pawn_x+1, rank_of_interest))
    players[ally_color].add_piece(
        ally_pawn,
        players[opponent_color],
    )
    players[ally_color].get_king().set_position((0, rank_of_interest))

    players[opponent_color].check_for_piece_selection(enemy_pawn.get_position())
    players[opponent_color].move_selected_piece(
        players[ally_color],
        (enemy_pawn_x, rank_of_interest),
    )

    en_passant_is_allowed = (
            bad_move
            in ally_pawn.find_legal_moves(
                players[ally_color],
                players[opponent_color],
                ally_color,
            )
    )

    players[ally_color].check_for_piece_selection(ally_pawn.get_position())
    moved = players[ally_color].move_selected_piece(
        players[opponent_color],
        bad_move,
    )

    assert not en_passant_is_allowed
    assert ally_pawn.get_position() == (enemy_pawn_x+1, rank_of_interest)
    assert enemy_pawn in players[opponent_color].get_piece_objects()
    assert not moved

