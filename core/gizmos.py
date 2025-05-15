from __future__ import annotations

import pygame
from core.collider2d import *

class Gizmos:
    enabled = True  # Toggle global du mode debug
    alpha = 100     # Niveau de transparence (0 à 255)

    @staticmethod
    def draw_collider(surface, collider: Collider2D, color=(0, 255, 0), width=1):
        if not Gizmos.enabled:
            return

        if isinstance(collider, RectCollider2D):
            Gizmos.draw_rect(surface, collider.get_rect(), color, width)

        elif isinstance(collider, CircleCollider2D):
            center = collider.get_center()
            Gizmos.draw_circle(surface, center, collider.radius, color, width)

        elif isinstance(collider, CapsuleCollider2D):
            Gizmos.draw_capsule(surface, collider, color, width)

    @staticmethod
    def draw_rect(surface, rect, color, width=1):
        if width == 0:
            # Filled with alpha
            temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            temp.fill((*color, Gizmos.alpha))
            surface.blit(temp, rect.topleft)
        else:
            pygame.draw.rect(surface, color, rect, width)

    @staticmethod
    def draw_circle(surface, center, radius, color, width=1):
        if width == 0:
            temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp, (*color, Gizmos.alpha), (radius, radius), radius)
            surface.blit(temp, (center.x - radius, center.y - radius))
        else:
            pygame.draw.circle(surface, color, (int(center.x), int(center.y)), int(radius), width)

    @staticmethod
    def draw_capsule(surface, capsule, color, width=1):
        rect, circle1, circle2 = capsule.get_rect_and_circles()
        Gizmos.draw_rect(surface, rect, color, width)
        Gizmos.draw_circle(surface, circle1, capsule.radius, color, width)
        Gizmos.draw_circle(surface, circle2, capsule.radius, color, width)

    @staticmethod
    def toggle():
        Gizmos.enabled = not Gizmos.enabled

#class GizmosUIButton:
#    def __init__(self, position=(10, 10), size=(120, 32)):
#        self.position = pygame.Vector2(position)
#        self.size = pygame.Vector2(size)
#        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
#        self.font = pygame.font.SysFont('Arial', 16)
#        self.bg_color_on = (0, 180, 0)
#        self.bg_color_off = (100, 100, 100)
#        self.text_color = (255, 255, 255)
#
#    def handle_event(self, event):
#        if event.type == pygame.MOUSEBUTTONDOWN:
#            if self.rect.collidepoint(event.pos):
#                Gizmos.toggle()
#
#    def draw(self, surface):
#        color = self.bg_color_on if Gizmos.enabled else self.bg_color_off
#        pygame.draw.rect(surface, color, self.rect, border_radius=6)
#        label = "Gizmos: ON" if Gizmos.enabled else "Gizmos: OFF"
#        text_surface = self.font.render(label, True, self.text_color)
#        text_rect = text_surface.get_rect(center=self.rect.center)
#        surface.blit(text_surface, text_rect)