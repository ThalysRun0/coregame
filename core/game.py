from abc import abstractmethod
import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.scene_manager import SceneManager
from core.sound_manager import SoundManager
from core.input import Input

class Game:

    def __init__(self, root, width=DEFAULT_CORE_SCREEN_WIDTH, height=DEFAULT_CORE_SCREEN_HEIGHT, fps=DEFAULT_CORE_FPS):
        pygame.init()
        self.debug = Debug(root, max_messages=DEFAULT_CORE_DEBUG_MAX_MESSAGES)
        if DEFAULT_CORE_DEBUG: self.debug.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}->({width}, {height})")
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False
        self.fps = fps
        self.fixed_delta_time = 1.0 / DEFAULT_CORE_FIXED_FPS
        self.accumulator = 0.0

        self.scene_manager = SceneManager(self.screen)
        self.sound_manager = SoundManager()
        self.load_sound()
        self.start()

    @abstractmethod
    def load_sound(self):
        pass

    @abstractmethod
    def start(self):
        pass

    def run(self):
        if DEFAULT_CORE_DEBUG: self.debug.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        while self.running:
            events = pygame.event.get()
            Input.update(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                self.scene_manager.handle_event(event)

            delta_time = self.clock.tick(self.fps) / 1000.0
            self.scene_manager.update(delta_time)

            self.accumulator += delta_time
            while self.accumulator >= self.fixed_delta_time:
                self.scene_manager.fixed_update(self.fixed_delta_time)
                self.accumulator -= self.fixed_delta_time

            self.screen.fill(BLACK)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()