from collections.abc import Callable

import pytest

from player import Player


@pytest.fixture
def players_setup() -> Callable[[str, str], tuple[dict[str, Player], str]]:
    """
    Returns a function (_player_setup) that takes the arguments: piece_setup, color_to_move
    """
    def _player_setup(piece_setup: str, color_to_move: str='w') -> tuple[dict[str, Player], str]:
        """
        Returns tuple(players, opponent_color, pawn_diraction)
        """
        return (
                { # players dict
                'w': Player('w', piece_setup=piece_setup),
                'b': Player('b', piece_setup=piece_setup),
                },
                'w' if color_to_move == 'b' else 'b', # opponent color
                )
    return _player_setup

