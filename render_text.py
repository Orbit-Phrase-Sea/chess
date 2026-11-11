"""Module containing a function that renders the game result."""

import pygame

from constants import Display


def render_text(text: str) -> pygame.surface.Surface:
    """Render the appropriate result and return the surface."""
    pygame.font.init()

    text_font = pygame.font.Font(Display.FONT_PATH, 85)
    text_surface = text_font.render(text, False, (255,)*3)
    text_surface.set_alpha(220)
    return text_surface

