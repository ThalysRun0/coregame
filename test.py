import os

import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.game import Game
from core.scene import Scene
from core.input import Input
from core.gameobject import Gameobject
from core.gizmos import Gizmos
from core.collider2d import CircleCollider2D, CapsuleCollider2D
from core.rigidbody2d import Rigidbody2D

class thisScene(Scene):
    def __init__(self, screen):
        super().__init__("main_scene", screen)
        self.ball = self.Ball("ball", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2/2, self.screen.get_height()/2))
        self.player1 = self.Paddle("player1", self.screen, self.main_camera, pygame.Vector2(10, self.screen.get_height()/2))
        self.player2 = self.Paddle("player2", self.screen, self.main_camera, pygame.Vector2(760, self.screen.get_height()/2))

    def start(self):
        self.sprites.add(self.player1, self.player2, self.ball)
        #pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))

    def update(self, delta_time):
        super().update(delta_time)
        if self.player1.collider.check_collision(self.ball.collider):
            self.ball.rigidbody.velocity *= -1
        if self.player2.collider.check_collision(self.ball.collider):
            self.ball.rigidbody.velocity *= -1
        if Input.get_key_down(pygame.K_SPACE):
            self.toggle_pause()
        if Input.get_key_down(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen=None):
        super().draw(screen)
        #Debug.main.draw(screen)
        #Debug.debug_grid_vertical(screen, 100)
        line = 0
        Debug.debug_on_screen(screen, 0, line, f"(screen: {self.screen.get_clip()})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(ball_velocity: {self.ball.rigidbody.velocity})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(ball_position: {self.ball.position})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(player1_position: {self.player1.position})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(player2_position: {self.player2.position})", WHITE, False)


    class Ball(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2, radius=10):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(radius*2, radius*2))
            self.radius = radius
            self.collider = CircleCollider2D(self, self.radius)
            self.rigidbody = Rigidbody2D(self, use_gravity=False)
            self.start()

        def start(self):
            self.rigidbody.apply_force(pygame.Vector2(100, -100))

        def update(self, delta_time):
            super().update(delta_time)
            self.rigidbody.update(delta_time)

            if self.screen_pos.y <= 0 or self.screen_pos.y + self.size.y >= self.screen.get_height():
                self.rigidbody.velocity.y *= -1

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.circle(screen, WHITE, self.get_center(), self.radius)
            Gizmos.draw_collider(screen, self.collider, GREEN)


    class Paddle(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(20, 100))
            self.collider = CapsuleCollider2D(self, 10)

        def update(self, delta_time):
            super().update(delta_time)
            if Input.get_key(pygame.K_UP):
                self.position.y -= 10
            if Input.get_key(pygame.K_DOWN):
                self.position.y += 10

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.rect(screen, WHITE, self.rect)
            Gizmos.draw_collider(screen, self.collider, GREEN)


class thisGame(Game):
    def start(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.scene_manager.load_scene(thisScene(self.screen))

    def load_sound(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        sound_folder = os.path.join(os.path.dirname(__file__), "assets", "sounds")
        self.sound_manager.load("on", f"{sound_folder}/on.ogg")
        self.sound_manager.load("off", f"{sound_folder}/off.ogg")
        self.sound_manager.load("bounce", f"{sound_folder}/button2.ogg")

game = thisGame("./logs/")
game.run()
