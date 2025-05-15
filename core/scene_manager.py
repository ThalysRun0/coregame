import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.scene import Scene

class SceneManager:
    def __init__(self, screen: pygame.surface):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.screen = screen
        self.current_scene: Scene = None

    def load_scene(self, scene: Scene):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.current_scene = scene
        self.current_scene.start()

    def draw(self, screen: pygame.surface):
        if self.current_scene:
            self.current_scene.draw(screen)

    def update(self, delta_time):
        if self.current_scene:
            self.current_scene.update(delta_time)
    
    def fixed_update(self, fixed_delta_time):
        if self.current_scene:
            self.current_scene.update(fixed_delta_time)

    def handle_event(self, event: pygame.event.Event):
        if self.current_scene:
            self.current_scene.handle_event(event)