from abc import abstractmethod
import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.camera import Camera
from core.gameobject import Gameobject

class Scene:
    def __init__(self, name, screen: pygame.Surface):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}({name})")
        self.name = name
        self.screen = screen
        self.sprites = pygame.sprite.Group()
        self.started = False
        self.main_camera = Camera(self.screen)
        self.pause = False

    def start(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        for sprite in self.sprites:
            sprite: Gameobject = sprite
            sprite.start()
        self.started = True
    
    def update(self, delta_time):
        if not self.pause:
            for sprite in self.sprites:
                sprite: Gameobject = sprite
                sprite.update(delta_time)

    def fixed_update(self, fixed_delta_time):
        if not self.pause:
            for sprite in self.sprites:
                sprite: Gameobject = sprite
                sprite.fixed_update(fixed_delta_time)

    def draw(self, screen: pygame.Surface):
        #self.sprites.draw(screen)
        for sprite in self.sprites:
            sprite: Gameobject = sprite
            sprite.draw(screen, self.main_camera)

    def toggle_pause(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> pause:{not self.pause}")
        self.pause = not self.pause

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass