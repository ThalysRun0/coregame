import pygame

from core.input import Input

def test_input_random():
    Input.update([pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})])
    assert Input.get_key_down(pygame.K_SPACE)