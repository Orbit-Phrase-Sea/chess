import pytest

from player import Player


@pytest.fixture
def players_setup():
    def _player_setup(piece_setup):
        return {
                'w': Player('w', piece_setup=piece_setup),
                'b': Player('b', piece_setup=piece_setup),
                }
    return _player_setup

