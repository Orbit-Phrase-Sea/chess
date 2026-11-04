import pytest

from player import Player


@pytest.fixture
def players_setup():
    def _player_setup(piece_setup, color_to_move='w'):
        return {
                'w': Player('w', piece_setup=piece_setup),
                'b': Player('b', piece_setup=piece_setup),
                }, 'w' if color_to_move == 'b' else 'b'
    return _player_setup

