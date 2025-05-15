import inspect
import pygame

from core.constants import *
from core.debug import Debug

class Camera:
    main = None

    def __new__(cls, *args, **kwargs):
        if cls.main is None:
            cls.main = super(Camera, cls).__new__(cls)
        return cls.main
    
    def __init__(self, screen: pygame.Surface, position=(0, 0)):
        if hasattr(self, '_initialized') and self._initialized:
            return
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.position = pygame.Vector2(position)
        self.screen = screen
        self.zoom = 1.0
        self._initialized = True

    def world_to_screen(self, world_pos):
        screen_x = (world_pos.x - self.position.x)
        screen_y = (world_pos.y - self.position.y)
        return pygame.Vector2(screen_x, screen_y)

    def follow(self, target_pos):
        self.position = pygame.Vector2(target_pos) - pygame.Vector2(self.screen.get_size()) / 2