import os

import inspect
import pygame
from random import randint

from core.constants import *
from core.debug import Debug
from core.game import Game
from core.scene import Scene
from core.input import Input
from core.gameobject import Gameobject
from core.gizmos import Gizmos
from core.collider2d import Collider2D, RectCollider2D, CircleCollider2D, Hits, Hit
from core.rigidbody2d import Rigidbody2D

class MainScene(Scene):
    COUNTDOWN_EVENT = pygame.USEREVENT + 1

    def __init__(self, screen):
        super().__init__("main_scene", screen)
        self.unincr = self.UnIncr("unincr", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2), size=(100, 50))
        self.ball = self.Ball("ball", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2/2, self.screen.get_height()/2))
        self.player1 = self.Paddle("player1", self.screen, self.main_camera, pygame.Vector2(20, self.screen.get_height()/2))
        self.player2 = self.Paddle("player2", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()-40, self.screen.get_height()/2))
        self.top_wall = self.Wall("top_wall", self.screen, self.main_camera, pygame.Vector2(0, 0), pygame.Vector2(self.screen.get_width(), 20))
        self.bottom_wall = self.Wall("bottom_wall", self.screen, self.main_camera, pygame.Vector2(0, self.screen.get_height()-20), pygame.Vector2(self.screen.get_width(), 20))
        self.sprites.add(self.player1, self.player2, self.ball, self.top_wall, self.bottom_wall, self.unincr)
        self.multi_ball = []
        self.scores = (0, 0)

    def start(self):
        super().start()
        self.ball.position = pygame.Vector2(self.screen.get_width()/2/2, self.screen.get_height()/2)
        self.ball.rigidbody.velocity = pygame.Vector2(0, 0)
        self.unincr.value = 3
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"scene": "unincr"}))
        pygame.time.set_timer(self.COUNTDOWN_EVENT, 1000)

    def play(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.unincr.active = False
        self.ball.rigidbody.apply_force(pygame.Vector2(200, -150))

    def update(self, delta_time):
        super().update(delta_time)

        self.check_collision()
        while len(Hits.hits) > 0:
            hit: Hit = Hits.pop_hit()
            if hit.collided:
                if isinstance(hit.other.parent, self.Ball):
                    hit.other.parent.rigidbody.velocity = hit.other.parent.rigidbody.velocity.reflect(hit.normal)

        if self.ball.screen_pos.x + self.ball.size.x <= 0 or self.ball.screen_pos.x - self.ball.size.x >= self.screen.get_width():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "restart"}))

        for tmp_ball in self.multi_ball:
            if tmp_ball.screen_pos.x + tmp_ball.size.x <= 0 or tmp_ball.screen_pos.x - tmp_ball.size.x >= self.screen.get_width():
                self.multi_ball.remove(tmp_ball)
                self.sprites.remove(tmp_ball)

    # TODO: need refinement
    def add_multi_ball(self):
        self.multi_ball = []
        for i in range(1, 5):
            new_ball = self.Ball(f"ball{i}", self.screen, self.main_camera, self.ball.position)
            new_ball.rigidbody.apply_force(pygame.Vector2(randint(-149, 149), randint(-99, 99)))
            self.multi_ball.append(new_ball)
        self.sprites.add(self.multi_ball)

    def handle_event(self, event):
        super().handle_event(event)

        if Input.get_key_down(pygame.K_SPACE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "pause"}))
        if Input.get_key_down(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "quit"}))
        if Input.get_key_down(pygame.K_F1):
            Gizmos.toggle()
        if Input.get_key_down(pygame.K_F2):
            self.add_multi_ball()

        if event.type == self.COUNTDOWN_EVENT:
            self.unincr.value -= 1
            if self.unincr.value <= 0:
                pygame.time.set_timer(self.COUNTDOWN_EVENT, 0)
                self.play()

        if event.type == pygame.USEREVENT:
            if hasattr(event, 'scene'):
                if event.scene == "unincr":
                    pygame.time.set_timer(self.COUNTDOWN_EVENT, 1000)
            if hasattr(event, 'action'):
                if event.action == "pause":
                    self.toggle_pause()
                if event.action == "restart":
                    self.start()
                if event.action == "quit":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

#    def fixed_update(self, fixed_delta_time):
#        super().fixed_update(fixed_delta_time)

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


    class UnIncr(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2, size: pygame.Vector2, color=(255, 255, 255)):
            super().__init__(name, screen, camera, position, size)
            self.color = color
            self.value: int

        def start(self):
            super().start()
            self.fade_alpha = 255
            self.fade_speed = 85  # diminue par seconde (~3 steps de fade sur 1s)

        def update(self, delta_time):
            super().update(delta_time)
            self.fade_alpha = max(0, self.fade_alpha - self.fade_speed * delta_time)

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            font = pygame.font.Font(DEFAULT_FONTNAME, 80)
            fade_surface = pygame.Surface((screen.get_width()/2, screen.get_height()/2), pygame.SRCALPHA)
            text = font.render(str(self.value), True, (255, 255, 255))
            text.set_alpha(self.fade_alpha)
            fade_surface.blit(text, self.position)
            screen_rect = fade_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            screen.blit(fade_surface, screen_rect)
            pygame.display.update(screen_rect)


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
            self.rigidbody = Rigidbody2D(self, use_gravity=True)

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


class PongGame(Game):
    def __init__(self, root, width=800, height=600, fps=DEFAULT_CORE_FPS):
        super().__init__(root, width, height, fps)

    def start(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.scene_manager.load_scene(MainScene(self.screen))

    def load_sound(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        sound_folder = os.path.join(os.path.dirname(__file__), "assets", "sounds")
        self.sound_manager.load("on", f"{sound_folder}/on.ogg")
        self.sound_manager.load("off", f"{sound_folder}/off.ogg")
        self.sound_manager.load("bounce", f"{sound_folder}/button2.ogg")

game = PongGame("./logs/")
game.run()
