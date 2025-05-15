import os
import datetime
import pygame

from core.constants import *

class Debug:
    main = None

    def __new__(cls, *args, **kwargs):
        if cls.main is None:
            cls.main = super(Debug, cls).__new__(cls)
        return cls.main
    
    def __init__(self, root, font=None, max_messages=10, x=10, y=10, line_spacing=5, color=(255, 255, 255)):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.folderpath = os.path.dirname(root)
        self.filepath = os.path.join(self.folderpath, f"core.debug.{datetime.date.isoformat(datetime.datetime.now())}.{datetime.date.strftime(datetime.datetime.now(), "%H%M%S")}")
        if DEFAULT_CORE_DEBUG: print(f"LOG file initialization : {self.filepath}")
        if DEFAULT_CORE_DEBUG: print(f"font initialization : ({DEFAULT_FONTNAME}, {DEFAULT_FONTSIZE})")
        if font is None:
            font = pygame.font.Font(DEFAULT_FONTNAME, DEFAULT_FONTSIZE)
        self.font = font
        self.max_messages = max_messages
        self.messages = []
        self.x = x
        self.y = y
        self.line_spacing = line_spacing
        self.color = color
        self._initialized = True

    def log(self, message):
        with open(self.filepath, 'a') as f:
            f.write(f"{datetime.datetime.now()}-{len(self.messages)}-{message}\n")
        
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def draw(self, surface: pygame.Surface = None):
        for i, msg in enumerate(reversed(self.messages)):
            text_surface = self.font.render(msg, True, self.color)
            surface.blit(text_surface, (self.x, self.y + i * (text_surface.get_height() + self.line_spacing)))

    @staticmethod
    def debug_on_screen(screen: pygame.Surface, x, y, message, color=WHITE, antialias=True):
        font = pygame.font.Font(DEFAULT_FONTNAME, DEFAULT_FONTSIZE)
        text_surface = font.render(message, antialias, color)
        screen.blit(text_surface, (x, y * text_surface.get_height()))
    
    @staticmethod
    def debug_grid_vertical(screen: pygame.Surface, max=50):
        # a grid for vertical coord in debug
        for i in range(0, max):
            Debug.debug_on_screen(screen, screen.get_width()-25, i, f"{i} -", WHITE, False)