import pytest

from pieces import King
from pieces import Queen
from pieces import Rook
from pieces import Bishop
from pieces import Knight
from pieces import Pawn


@pytest.mark.parametrize('piece_class', [King, Queen, Rook, Bishop, Knight, Pawn])
@pytest.mark.parametrize('color', ['w', 'b'])
@pytest.mark.parametrize('file', [-1, 8])
@pytest.mark.parametrize('rank', [-1, 8])
def test_piece_init(piece_class, color, file, rank):
    with pytest.raises(ValueError):
        piece_class(color, (file, rank))

