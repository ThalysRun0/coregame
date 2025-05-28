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

CELL_SIZE = 20

class MainScene(Scene):
    COUNTDOWN_EVENT = pygame.USEREVENT + 1

    def __init__(self, screen):
        super().__init__("main_scene", screen)
        self.unincr = self.UnIncr("unincr", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2), size=(100, 50))
        self.player1 = self.Snake("player1", self.screen, self.main_camera, pygame.Vector2(20, self.screen.get_height()/2))
        self.walls = []
        self.walls.append(self.Wall("top_wall", self.screen, self.main_camera, pygame.Vector2(0, 0), pygame.Vector2(self.screen.get_width(), 20)))
        self.walls.append(self.Wall("left_wall", self.screen, self.main_camera, pygame.Vector2(0, 20), pygame.Vector2(20, self.screen.get_height()-40)))
        self.walls.append(self.Wall("right_wall", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()-20, 20), pygame.Vector2(20, self.screen.get_height()-40)))
        self.walls.append(self.Wall("bottom_wall", self.screen, self.main_camera, pygame.Vector2(0, self.screen.get_height()-20), pygame.Vector2(self.screen.get_width(), 20)))
        
        self.foods = []
        self.sprites.add(self.player1, self.walls)
        self.scores: int = 0
        self.restart(0)

    def start(self):
        super().start()
        pygame.time.set_timer(self.COUNTDOWN_EVENT, 1000)

    def restart(self, score_added: int):
        self.unincr.value = 3
        self.foods.clear()
        self.add_food("food_1")
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "start"}))

    def play(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.unincr.active = False

    def add_food(self, name):
        new_food = self.Food(name, self.screen, self.main_camera, pygame.Vector2(0, 0))
        new_food.spawn()
        self.foods.append(new_food)
        self.sprites.add(new_food)
        return new_food

    def update(self, delta_time):
        super().update(delta_time)

        self.check_collision()
        while len(Hits.hits) > 0:
            hit: Hit = Hits.pop_hit()
            if hit.collided:
                if isinstance(hit.other.parent, self.Food):
                    self.player1.grow()

    def handle_event(self, event):
        super().handle_event(event)

        if Input.get_key_down(pygame.K_SPACE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "pause"}))
        if Input.get_key_down(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "quit"}))
        if Input.get_key_down(pygame.K_F1):
            Gizmos.toggle()

        if event.type == self.COUNTDOWN_EVENT:
            self.unincr.value -= 1
            if self.unincr.value <= 0:
                pygame.time.set_timer(self.COUNTDOWN_EVENT, 0)
                self.play()

        if event.type == pygame.USEREVENT:
            if hasattr(event, 'action'):
                if event.action == "pause":
                    self.toggle_pause()
                if event.action == "restart":
                    self.restart(0)
                if event.action == "start":
                    self.start()
                if event.action == "quit":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        super().draw(screen)
        #Debug.main.draw(screen)
        #Debug.debug_grid_vertical(screen, 100)
        Debug.line = 2
        Debug.debug_on_screen(screen, 0, Debug.line, f"{self.scores}", WHITE, True)
        Debug.debug_on_screen(screen, 0, Debug.line, f"{self.unincr.value}", WHITE, True)
#        Debug.debug_on_screen(screen, 0, Debug.line, f"(ball_velocity: {self.ball.rigidbody.velocity})", WHITE, False)
#        Debug.debug_on_screen(screen, 0, Debug.line, f"(ball_position: {self.ball.position})", WHITE, False)
#        Debug.debug_on_screen(screen, 0, Debug.line, f"(player1_position: {self.player1.position})", WHITE, False)
#        Debug.debug_on_screen(screen, 0, Debug.line, f"(player2_position: {self.player2.position})", WHITE, False)


    class UnIncr(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2, size: pygame.Vector2, color=(255, 255, 255)):
            super().__init__(name, screen, camera, position, size)
            self.color = color
            self.value: int = 3

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


    class Food(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(20, 20))
            self.collider = RectCollider2D(self)
            self.value = 1

        def spawn(self):
            self.position = pygame.Vector2(randint(0, self.screen.get_width()-1), randint(0, self.screen.get_height()-1))

        def on_collision(self, hit):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "score", "add": f"{str(self.value)}"}))
            self.spawn()

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.rect(screen, WHITE, self.get_rect())
            Gizmos.draw_collider(screen, self.collider, GREEN, 0)


    class Snake(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(20, 100))
            self.collider = RectCollider2D(self)
            self.direction = pygame.Vector2(0, 0)
            self.snake = [(10, 10), (9, 10), (8, 10)]

        def update(self, delta_time):
            super().update(delta_time)
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])

            # Collision mur ou soi-même
            if (new_head in self.snake) or not (0 <= new_head[0] < self.screen.get_width()) or not (0 <= new_head[1] < self.screen.get_height()):
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "restart"}))

            self.snake.insert(0, new_head)
            self.snake.pop()

        def grow(self):
            pass

        def handle_event(self, event):
            super().handle_event(event)
            if Input.get_key_up(pygame.K_UP) and self.direction != (0, 1):
                self.direction = (0, -1)
            if Input.get_key_up(pygame.K_DOWN) and self.direction != (0, -1):
                self.direction = (0, 1)
            if Input.get_key_up(pygame.K_LEFT) and self.direction != (1, 0):
                self.direction = (-1, 0)
            if Input.get_key_up(pygame.K_RIGHT) and self.direction != (-1, 0):
                self.direction = (1, 0)

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            length = len(self.snake)
            for i, segment in enumerate(self.snake):
                if i == 0:
                    color = (0, 255, 0)  # Tête - vert fluo
                elif i == len(self.snake) - 1:
                    color = (80, 120, 60)  # Queue - vert olive/marron
                else:
                    fade_factor = 1 - (i / length)  # 1.0 (tête) → 0.0 (queue)
                    alpha = int(255 * fade_factor)  # 255 (opaque) → 0 (transparent)
                    color = (0, 255, 0, alpha)  # RGBA
                
                rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
#            pygame.draw.rect(screen, WHITE, self.rect)
#            Gizmos.draw_collider(screen, self.collider, GREEN, 0)


class SnakeGame(Game):
    def __init__(self, root, width=800, height=600, fps=10):
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

game = SnakeGame("./logs/")
game.run()
