"""All chess project constants are defined here."""

from os import path
from dataclasses import dataclass


@dataclass(frozen=True)
class Display:
    """Display related constants."""

    WIDTH: int = 800
    HEIGHT: int = 800
    FPS: int = 20
    CHECK_INDICATOR_IMAGE_PATH: str = path.join('assets', 'check_indicators', 'red_blur.png')
    BOARD_IMAGE_PATH: str = path.join('assets', 'boards', 'maple.jpg')
    PIECE_THEME_ROOT_PATH: str = path.join('assets', 'piece_sets', 'cburnett')
    FONT_PATH: str = path.join('assets', 'fonts', 'nunito', 'Nunito-ExtraBold.ttf')

