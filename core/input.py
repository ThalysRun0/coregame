from typing import List

import inspect
import pygame

from core.constants import *
from core.debug import Debug

class Input:
    keys_down = set()
    keys_up = set()
    keys_held = set()

    @staticmethod
    def update(events: List[pygame.event.Event]):
        Input.keys_down.clear()
        Input.keys_up.clear()

        for event in events:
            if event.type == pygame.KEYDOWN:
                #if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}.event.KEYDOWN")
                key = event.key
                if key not in Input.keys_held:
                    Input.keys_down.add(key)
                    Input.keys_held.add(key)
            elif event.type == pygame.KEYUP:
                #if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}.event.KEYUP")
                key = event.key
                Input.keys_up.add(key)
                if key in Input.keys_held:
                    #if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}.event.KEYHELD")
                    Input.keys_held.remove(key)

    @staticmethod
    def get_key(key):
        if key in Input.keys_held:
            #if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}({key})")
            return True
        
    @staticmethod
    def get_key_down(key):
        if key in Input.keys_down:
            #if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}({key})")
            return True
    
    @staticmethod
    def get_key_up(key):
        if key in Input.keys_up:
            #if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}({key})")
            return True
    
