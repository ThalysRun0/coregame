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
from core.collider2d import Collider2D, RectCollider2D, CircleCollider2D, Hits, Hit
from core.rigidbody2d import Rigidbody2D

class thisScene(Scene):
    def __init__(self, screen):
        super().__init__("main_scene", screen)
        self.ball = self.Ball("ball1", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2/2, self.screen.get_height()/2))
        self.player1 = self.Paddle("player1", self.screen, self.main_camera, pygame.Vector2(20, self.screen.get_height()/2))
        self.player2 = self.Paddle("player2", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()-40, self.screen.get_height()/2))
        self.top_wall = self.Wall("top_wall", self.screen, self.main_camera, pygame.Vector2(0, 0), pygame.Vector2(self.screen.get_width(), 20))
        self.bottom_wall = self.Wall("bottom_wall", self.screen, self.main_camera, pygame.Vector2(0, self.screen.get_height()-20), pygame.Vector2(self.screen.get_width(), 20))
        self.sprites.add(self.player1, self.player2, self.ball, self.top_wall, self.bottom_wall)

    def start(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.ball.position = pygame.Vector2(self.screen.get_width()/2/2, self.screen.get_height()/2)
        self.ball.rigidbody.velocity = pygame.Vector2(0, 0)
        self.ball.rigidbody.apply_force(pygame.Vector2(150, -100))

    def update(self, delta_time):
        super().update(delta_time)

#        self.check_collision() # TODO: need refinement
#        while len(Hits.hits) > 0:
#            hit: Hit = Hits.pop_hit()
#            if hit.collided:
#                if isinstance(hit.self.parent, self.Ball):
#                    hit.self.parent.rigidbody.velocity = hit.self.parent.rigidbody.velocity.reflect(hit.normal)

        player1_hit: Hit = self.player1.collider.check_collision(self.ball.collider)
        player2_hit: Hit = self.player2.collider.check_collision(self.ball.collider)
        if player1_hit.collided:
            Gizmos.add_hit(player1_hit, color=(255, 0, 0), normal_scale=20, duration=2.0)
            self.ball.rigidbody.velocity = self.ball.rigidbody.velocity.reflect(player1_hit.normal)
        if player2_hit.collided:
            Gizmos.add_hit(player2_hit, color=(255, 0, 0), normal_scale=20, duration=2.0)
            self.ball.rigidbody.velocity = self.ball.rigidbody.velocity.reflect(player2_hit.normal)
        
        top_wall_hit: Hit = self.top_wall.collider.check_collision(self.ball.collider)
        bottom_wall_hit: Hit = self.bottom_wall.collider.check_collision(self.ball.collider)
        if top_wall_hit.collided:
            Gizmos.add_hit(top_wall_hit, color=(255, 0, 0), normal_scale=20, duration=2.0)
            self.ball.rigidbody.velocity = self.ball.rigidbody.velocity.reflect(top_wall_hit.normal)
        if bottom_wall_hit.collided:
            Gizmos.add_hit(bottom_wall_hit, color=(255, 0, 0), normal_scale=20, duration=2.0)
            self.ball.rigidbody.velocity = self.ball.rigidbody.velocity.reflect(bottom_wall_hit.normal)

        if self.ball.screen_pos.x + self.ball.size.x <= 0 or self.ball.screen_pos.x - self.ball.size.x >= self.screen.get_width():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "restart"}))

    def handle_event(self, event):
        super().handle_event(event)

        if Input.get_key_down(pygame.K_SPACE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "pause"}))
        if Input.get_key_down(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "quit"}))
        if Input.get_key_down(pygame.K_F1):
            Gizmos.toggle()

        if event.type == pygame.USEREVENT:
            if event.action == "pause":
                self.toggle_pause()
            if event.action == "restart":
                self.start()
            if event.action == "quit":
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        super().draw(screen)
        #Debug.main.draw(screen)
        #Debug.debug_grid_vertical(screen, 100)
        line = 2
        Debug.debug_on_screen(screen, 0, line, f"(ball_velocity: {self.ball.rigidbody.velocity})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(ball_position: {self.ball.position})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(player1_position: {self.player1.position})", WHITE, False)
        line += 1
        Debug.debug_on_screen(screen, 0, line, f"(player2_position: {self.player2.position})", WHITE, False)


    class Wall(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2, size: pygame.Vector2):
            super().__init__(name, screen, camera, position, size)
            self.collider = RectCollider2D(self)

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.rect(screen, WHITE, self.rect)
            Gizmos.draw_collider(screen, self.collider, GREEN, 0)


    class Ball(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2, radius=10):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(radius*2, radius*2))
            self.radius = radius
            self.collider = CircleCollider2D(self, self.radius)
            self.rigidbody = Rigidbody2D(self, use_gravity=False)

        def update(self, delta_time):
            super().update(delta_time)
            self.rigidbody.update(delta_time)

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.circle(screen, WHITE, self.get_center(), self.radius)
            Gizmos.draw_collider(screen, self.collider, GREEN, 0)


    class Paddle(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(20, 100))
            #self.collider = CapsuleCollider2D(self, 10)
            self.collider = RectCollider2D(self)

        def update(self, delta_time):
            super().update(delta_time)
            if Input.get_key(pygame.K_UP):
                self.position.y -= 10
            if Input.get_key(pygame.K_DOWN):
                self.position.y += 10

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.rect(screen, WHITE, self.rect)
            Gizmos.draw_collider(screen, self.collider, GREEN, 0)


class thisGame(Game):
    def __init__(self, root, width=800, height=600, fps=DEFAULT_CORE_FPS):
        super().__init__(root, width, height, fps)

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
