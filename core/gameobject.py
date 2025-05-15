from __future__ import annotations
from abc import abstractmethod
from typing import List

import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.camera import Camera

class Gameobject(pygame.sprite.Sprite):
    def __init__(self, name, screen: pygame.Surface=None, camera: Camera=None, position: pygame.Vector2=(0, 0), size: pygame.Vector2=(0, 0)):
        super().__init__()
        self.name = name
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}({name})")
        if camera is None:
            camera = Camera.main
        self.camera = camera
        self.screen = screen
        self.image = pygame.Surface(size)

        self.parent: Gameobject = None
        self.position = position
        self.size = size
        self.screen_pos = self.camera.world_to_screen(self.position)
        self.rect = pygame.Rect(self.screen_pos, self.size)

        self.active = True

    @abstractmethod
    def start(self):
        """to be called at the very end of __init__"""
        pass

    @abstractmethod
    def fixed_update(self, fixed_delta_time):
        if not self.active:
            return
        pass

    def update(self, delta_time):
        if not self.active:
            return
        self.screen_pos = self.camera.world_to_screen(self.position)
        self.rect = pygame.Rect(self.screen_pos, self.size)

    def draw(self, screen: pygame.Surface, camera:Camera):
        if not self.active:
            return

    def get_center(self, camera:Camera=None):
        if camera is None:
            camera = self.camera
        self.screen_pos = camera.world_to_screen(self.position)
        return pygame.Vector2(self.screen_pos.x + self.size.x / 2, self.screen_pos.y + self.size.y / 2)
