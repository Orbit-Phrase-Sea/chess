"""All chess project constants are defined here."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Display:
    """Display related constants."""

    WIDTH: int = 800
    HEIGHT: int = 800
    FPS: int = 20

