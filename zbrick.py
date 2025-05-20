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
import assets.levels as levels

class MainScene(Scene):
    COUNTDOWN_EVENT = pygame.USEREVENT + 1

    def __init__(self, screen):
        super().__init__("main_scene", screen)
        self.unincr = self.UnIncr("unincr", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2), size=(100, 50))
        self.player1 = self.Paddle("player1", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()-40))
        self.player1.is_sticky = True
        self.top_wall = self.Wall("top_wall", self.screen, self.main_camera, pygame.Vector2(0, 0), pygame.Vector2(self.screen.get_width(), 20))
        self.left_wall = self.Wall("left_wall", self.screen, self.main_camera, pygame.Vector2(0, 20), pygame.Vector2(20, self.screen.get_height()-40))
        self.right_wall = self.Wall("right_wall", self.screen, self.main_camera, pygame.Vector2(self.screen.get_width()-20, 20), pygame.Vector2(20, self.screen.get_height()-40))
        self.balls = []
        self.bricks = []
        self.level = 1
        self.init_level(self.level)

        self.sprites.add(self.player1, self.top_wall, self.left_wall, self.right_wall)
        self.scores: int = 0
        self.restart(self.scores)

    def init_level(self, level):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.sprites.remove(self.bricks)
        self.bricks.clear()

        if level == 1:
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 50)))
        if level == 2:
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 50)))
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick12_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 100)))
        if level == 3:
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 50)))
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick12_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 100)))
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick13_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 150)))
        if level == 4:
            for i in range(0, 10):
                self.bricks.append(self.Brick2(f"brick2_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 50)))
            for i in range(0, 10):
                self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2((i*60)+(self.screen.get_width()/10)+50, 100)))
#       if level == 5:
#           for i in range(1, 7):
#               if i % 2 == 0: # even
#                   for j in range(1, i+1):
#                       if j <= i/2:
#                           x = (self.screen.get_width()/2 - ((j*60)))
#                           y = (i*50)
#                           self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2(x, y)))
#                       else:
#                           x = (self.screen.get_width()/2 + (((i-j)*60)))
#                           y = (i*50)
#                           self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2(x, y)))
#               else: # odd
#                   for j in range(1, i+1):
#                       if j <= i/2:
#                           x = (self.screen.get_width()/2 - ((j*60))-30)
#                           y = (i*50)
#                           self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2(x, y)))
#                       else:
#                           x = (self.screen.get_width()/2 + (((i-j)*60))-30)
#                           y = (i*50)
#                           self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2(x, y)))
        if level >= 5:
            tmp = levels.levels[level]

            for i in range(0, len(tmp)):
                for j in range(0, len(tmp[i])):
                    if tmp[i][j] == 1:
                        self.bricks.append(self.Brick1(f"brick1_{i}", self.screen, self.main_camera, pygame.Vector2((j*60)+(self.screen.get_width()/10)+50, (i*30)+50)))
                    if tmp[i][j] == 2:
                        self.bricks.append(self.Brick2(f"brick2_{i}", self.screen, self.main_camera, pygame.Vector2((j*60)+(self.screen.get_width()/10)+50, (i*30)+50)))
                    if tmp[i][j] == 3:
                        self.bricks.append(self.Brick3(f"brick3_{i}", self.screen, self.main_camera, pygame.Vector2((j*60)+(self.screen.get_width()/10)+50, (i*30)+50)))

        # finalize
        self.sprites.add(self.bricks)


    def start(self):
        super().start()
        pygame.time.set_timer(self.COUNTDOWN_EVENT, 1000)

    def restart(self, score_added: int):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.scores = score_added
        self.player1.is_sticky = True
        self.unincr.value = 3
        self.sprites.remove(self.balls)
        self.balls.clear()
        new_ball = self.add_ball("ball_1", pygame.Vector2(self.screen.get_width()/2/2, self.screen.get_height()/2))
        new_ball.rigidbody.velocity = pygame.Vector2(0, 0)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "restart"}))

    def play(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.unincr.active = False

    def add_ball(self, name, position: pygame.Vector2):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        new_ball = self.Ball(name, self.screen, self.main_camera, position)
        self.balls.append(new_ball)
        self.sprites.add(new_ball)
        return new_ball

    # TODO: need refinement
#    def add_multi_ball(self):
#        for i in range(1, 5):
#            new_ball = self.add_ball(f"ball_{i+1}", pygame.Vector2(self.balls[0].position.x+20, self.balls[0].position.y+20))
#            new_ball.rigidbody.apply_force(pygame.Vector2(randint(-149, 149), randint(-99, 99)))
#            self.balls.append(new_ball)
#            self.sprites.add(new_ball)

    def level_update(self, update=1):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.level += update
        self.init_level(self.level)

    def update(self, delta_time):
        super().update(delta_time)

        if len(self.bricks) <= 0:
            pygame.event.clear()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "level", "update": 1}))

        self.check_collision()
        while len(Hits.hits) > 0:
            hit: Hit = Hits.pop_hit()
            if hit.collided:
                if (isinstance(hit.self.parent, self.Ball) and isinstance(hit.other.parent, self.Paddle)):
                    if hit.other.parent.is_sticky:
                        hit.self.parent.position = hit.other.parent.sticky_pos
                        continue
                if (isinstance(hit.self.parent, self.Paddle) and isinstance(hit.other.parent, self.Ball)):
                    if hit.self.parent.is_sticky:
                        hit.other.parent.position = hit.self.parent.sticky_pos
                        continue
                hit.self.parent.on_collision(hit)
                hit.other.parent.on_collision(hit)

        # quitting the bottom screen
        for tmp_ball in self.balls:
            tmp_ball: Gameobject = tmp_ball
            if tmp_ball.screen_pos.y + tmp_ball.size.y >= self.screen.get_height():
                self.balls.remove(tmp_ball)
                tmp_ball.destroy()
                if len(self.balls) <= 0:
                    self.restart(0)
        if self.player1.is_sticky:
            self.balls[0].position = self.player1.sticky_pos

    def handle_event(self, event):
        super().handle_event(event)
        if Input.get_key_up(pygame.K_SPACE):
            if self.player1.is_sticky:
                self.player1.is_sticky = False
                self.balls[0].rigidbody.velocity = pygame.Vector2(0, 0)
                self.balls[0].rigidbody.apply_force(pygame.Vector2(200, -150))
        if Input.get_key_up(pygame.K_p):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "pause"}))
        if Input.get_key_down(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "quit"}))
        if Input.get_key_up(pygame.K_F1):
            Gizmos.toggle()
        if Input.get_key_up(pygame.K_s):
            self.player1.is_sticky = not self.player1.is_sticky
        if Input.get_key_up(pygame.K_KP_PLUS):
            if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> key level_up")
 #           self.sprites.remove(self.bricks)
 #           self.bricks.clear()
            pygame.event.clear()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "level", "update": 1}))
        if Input.get_key_up(pygame.K_KP_MINUS):
            if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> key level_down")
#            self.sprites.remove(self.bricks)
#            self.bricks.clear()
            pygame.event.clear()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "level", "update": -1}))

#        if Input.get_key_up(pygame.K_m):
#            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "multi"}))

        if event.type == self.COUNTDOWN_EVENT:
            self.unincr.value -= 1
            if self.unincr.value <= 0:
                pygame.time.set_timer(self.COUNTDOWN_EVENT, 0)
                self.play()

        if event.type == pygame.USEREVENT:
            if hasattr(event, 'action'):
                if event.action == "level":
                    pygame.event.clear()
                    self.level_update(event.update)
                if event.action == "multi":
                    self.add_multi_ball()
                if event.action == "score":
                    if event.hit.self.parent in self.bricks:
                        self.scores += int(event.add)
                        self.bricks.remove(event.hit.self.parent)
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
        Debug.line = 2
        Debug.debug_on_screen(screen, 30, Debug.line, f"level : {self.level}", WHITE, True)
        Debug.debug_on_screen(screen, 30, Debug.line, f"score : {self.scores}", WHITE, True)
        Debug.debug_on_screen(screen, 30, Debug.line, f"decre : {self.unincr.value}", WHITE, True)
        Debug.debug_on_screen(screen, 30, Debug.line, f"Balls : {len(self.balls)}", WHITE, True)
        Debug.debug_on_screen(screen, 30, Debug.line, f"Bricks : {len(self.bricks)}", WHITE, True)
#        if len(self.balls)>0:
#            Debug.debug_on_screen(screen, 30, Debug.line, f"(ball_velocity: {self.balls[0].rigidbody.velocity})", WHITE, False)
#            Debug.debug_on_screen(screen, 30, Debug.line, f"(ball_position: {self.balls[0].position})", WHITE, False)
#        Debug.debug_on_screen(screen, 30, Debug.line, f"(player1_position: {self.player1.position})", WHITE, False)


    class UnIncr(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2, size: pygame.Vector2, color=(255, 255, 255)):
            super().__init__(name, screen, camera, position, size)
            self.color = color
            self.value: int = 0

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
            self.rigidbody = Rigidbody2D(self, use_gravity=False)

        def on_collision(self, hit):
            self.rigidbody.velocity = self.rigidbody.velocity.reflect(hit.normal)

        def update(self, delta_time):
            super().update(delta_time)
            self.rigidbody.update(delta_time)

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.circle(screen, WHITE, self.get_center(), self.radius)
            Gizmos.draw_collider(screen, self.collider, GREEN, 0)


    class Paddle(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(100, 20))
            self.collider = RectCollider2D(self)
            self.is_sticky = True
            self.sticky_pos = self.position

        def update(self, delta_time):
            super().update(delta_time)
            if Input.get_key(pygame.K_LEFT):
                self.position.x -= 10
            if Input.get_key(pygame.K_RIGHT):
                self.position.x += 10
            self.sticky_pos = pygame.Vector2(self.position.x+self.size.x-30, self.position.y-20)

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            color = (YELLOW if self.is_sticky else WHITE)
            pygame.draw.rect(screen, color, self.rect)
            Gizmos.draw_collider(screen, self.collider, GREEN, 0)

    class Brick1(Gameobject):
        def __init__(self, name, screen, camera, position: pygame.Vector2):
            super().__init__(name, screen, camera, position, size=pygame.Vector2(50, 20))
            self.collider = RectCollider2D(self)
            self.color = RED
            self.value = 1
            self.current_value = 0

        def start(self):
            self.current_value = self.value

        def on_collision(self, hit: Hit):
            self.current_value -= 1
            if self.current_value <= 0:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "score", "add": self.value, "hit": hit}))
                self.destroy()

        def draw(self, screen: pygame.Surface, camera):
            super().draw(screen, camera)
            pygame.draw.rect(screen, self.color, self.rect)
            #Gizmos.draw_collider(screen, self.collider, GREEN, 0)


    class Brick2(Brick1):
        def __init__(self, name, screen, camera, position):
            super().__init__(name, screen, camera, position)
            self.color = GREEN
            self.value = 2


    class Brick3(Brick1):
        def __init__(self, name, screen, camera, position):
            super().__init__(name, screen, camera, position)
            self.color = BLUE
            self.value = 3


class BrickGame(Game):
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

game = BrickGame("./logs/")
game.run()
