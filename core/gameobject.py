from __future__ import annotations
from abc import abstractmethod
from typing import List

import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.camera import Camera
from core.collider2d import *

class Gameobject(pygame.sprite.Sprite):
    def __init__(self, name, screen: pygame.Surface=None, camera: Camera=None, position: pygame.Vector2=(0, 0), size: pygame.Vector2=(0, 0)):
        super().__init__()
        self.name = name
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}({name})", DEBUG_CORE_INFO)
        if camera is None:
            camera = Camera.main
        self.camera = camera
        self.screen = screen
        self.image = pygame.Surface(size)

        self.parent: Gameobject = None
        self.position = position
        self.size = size
        print(f"init -> {__class__.__name__}:{type(self.position)}")
        self.screen_pos = self.camera.world_to_screen(self.position)
        self.rect = pygame.Rect(self.screen_pos, self.size)

        self.active = True

    @abstractmethod
    def start(self):
        """to be called at the very end of __init__
        ```super().start()
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def on_collision(self, hit: Hit=None):
        pass

    @abstractmethod
    def fixed_update(self, fixed_delta_time):
        if not self.active:
            return
        pass

    def destroy(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> destroy({self.name})")
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "destroy", "object": self}))

    def update(self, delta_time):
        if not self.active:
            return
        self.screen_pos = self.camera.world_to_screen(self.position)
        self.rect = pygame.Rect(self.screen_pos, self.size)

    def draw(self, screen: pygame.Surface, camera:Camera):
        if not self.active:
            return

    def get_center(self) -> pygame.Vector2:
        return self.position + self.size / 2

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

    def get_circle(self) -> pygame.Vector2:
        return pygame.Vector2(self.position.x + self.size.x / 2, self.position.y + self.size.y / 2)
