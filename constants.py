from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    WIDTH: int = 800
    HEIGHT: int = 800

