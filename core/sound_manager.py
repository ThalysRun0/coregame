import os

import inspect
import pygame

from core.constants import *
from core.debug import Debug

class SoundManager:
    def __init__(self, default_volume=1.0):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.sounds = {}
        self.default_volume = default_volume
        self.muted = False

    def load(self, name, path, volume=None):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        if not os.path.exists(path):
            if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__} - File not found : {path}")
            return
        
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume if volume is not None else self.default_volume)
        self.sounds[name] = sound

    def play(self, name):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        if self.muted:
            return
        sound:pygame.mixer.Sound = self.sounds.get(name)
        if sound:
            sound.play()
        else:
            if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__} - Sound not found : {name}")

    def stop(self, name):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        sound:pygame.mixer.Sound = self.sounds.get(name)
        if sound:
            sound.stop()
        else:
            if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__} - Sound not found : {name}")

    def set_volume(self, name, volume):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        sound:pygame.mixer.Sound = self.sounds.get(name)
        if sound:
            sound.set_volume(volume)
        else:
            if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__} - Sound not found : {name}")

    def toggle_mute(self):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}")
        self.muted = not self.muted