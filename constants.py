from dataclasses import dataclass


@dataclass(frozen=True)
class Display:
    WIDTH: int = 800
    HEIGHT: int = 800
    FPS: int = 20

