from abc import abstractmethod
import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.gizmos import Gizmos
from core.camera import Camera
from core.gameobject import Gameobject
from core.collider2d import Collider2D, Hits, Hit

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
        """to be called at the very beginning of your update method implementation
        ```super().update(delta_time)
        """
        Gizmos.update(delta_time)
        if not self.pause:
            for game_object in self.sprites:
                game_object: Gameobject = game_object
                game_object.update(delta_time)

    def check_collision(self):
        if not self.pause:
            for game_object in self.sprites:
                game_object: Gameobject = game_object
                if hasattr(game_object, "collider"):
                    game_collider: Collider2D = game_object.collider
                    for other_object in self.sprites:
                        other_object: Gameobject = other_object
                        if game_object != other_object:
                            if hasattr(other_object, "collider"):
                                other_collider: Collider2D = other_object.collider
                                hit: Hit = game_collider.check_collision(other_collider)
                                if hit.collided:
                                    Hits.add_hit(hit)
                                    Gizmos.add_hit(hit, color=(255, 0, 0), normal_scale=20, duration=2.0)

    def fixed_update(self, fixed_delta_time):
        if not self.pause:
            for sprite in self.sprites:
                sprite: Gameobject = sprite
                sprite.fixed_update(fixed_delta_time)

    def draw(self, screen: pygame.Surface):
        Gizmos.draw(screen)
        for sprite in self.sprites:
            sprite: Gameobject = sprite
            sprite.draw(screen, self.main_camera)

    def toggle_pause(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> pause:{not self.pause}")
        self.pause = not self.pause

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass