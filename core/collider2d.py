from __future__ import annotations

import inspect
import pygame
from abc import ABC, abstractmethod

from core.constants import *
from core.debug import Debug
from core.gameobject import Gameobject

class Collider2D(ABC):
    def __init__(self, parent: Gameobject, is_trigger=False):
        self.parent = parent
        self.is_trigger = is_trigger

    def get_center(self):
        return self.parent.get_center()

    @abstractmethod
    def check_collision(self, other: Collider2D):
        pass


class RectCollider2D(Collider2D):
    def __init__(self, parent: Gameobject, is_trigger=False):
        super().__init__(parent, is_trigger)
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}->parent({parent.name})")

    def get_rect(self):
        pos: pygame.Vector2 = self.parent.position
        size: pygame.Vector2 = self.parent.size
        return pygame.Rect(pos.x, pos.y, size.x, size.y)

    def check_collision(self, other: Collider2D):
        if isinstance(other, RectCollider2D):
            return self.get_rect().colliderect(other.get_rect())
        elif isinstance(other, CircleCollider2D):
            return other.check_collision(self)
        elif isinstance(other, CapsuleCollider2D):
            return other.check_collision(self)
        return False


class CircleCollider2D(Collider2D):
    def __init__(self, parent: Gameobject, radius, is_trigger=False):
        super().__init__(parent, is_trigger)
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}->parent({parent.name})")
        self.radius = radius

    def check_collision(self, other: Collider2D):
        if isinstance(other, CircleCollider2D):
            return self.get_center().distance_to(other.get_center()) < (self.radius + other.radius)

        elif isinstance(other, RectCollider2D):
            circle_center = self.get_center()
            rect = other.get_rect()
            closest_x = max(rect.left, min(circle_center.x, rect.right))
            closest_y = max(rect.top, min(circle_center.y, rect.bottom))
            distance = circle_center.distance_to(pygame.Vector2(closest_x, closest_y))
            return distance < self.radius

        elif isinstance(other, CapsuleCollider2D):
            return other.check_collision(self)

        return False


class CapsuleCollider2D(Collider2D):
    def __init__(self, parent: Gameobject, radius, orientation='vertical', is_trigger=False):
        super().__init__(parent, is_trigger)
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}->parent({parent.name})")
        self.radius = radius
        self.orientation = orientation  # 'vertical' or 'horizontal'

    def get_rect_and_circles(self):
        pos: pygame.Vector2 = self.parent.position
        size: pygame.Vector2 = self.parent.size
        if self.orientation == 'vertical':
            # Rectangle central (hauteur - 2*radius)
            rect_height = size.y - 2 * self.radius
            center_x = pos.x + size.x / 2
            top_circle = pygame.Vector2(center_x, pos.y + self.radius)
            bottom_circle = pygame.Vector2(center_x, pos.y + size.y - self.radius)
            rect = pygame.Rect(pos.x, pos.y + self.radius, size.x, rect_height)
            return rect, top_circle, bottom_circle
        else:  # horizontal
            rect_width = size.x - 2 * self.radius
            center_y = pos.y + size.y / 2
            left_circle = pygame.Vector2(pos.x + self.radius, center_y)
            right_circle = pygame.Vector2(pos.x + size.x - self.radius, center_y)
            rect = pygame.Rect(pos.x + self.radius, pos.y, rect_width, size.y)
            return rect, left_circle, right_circle

    def check_collision(self, other: Collider2D):
        rect, circle1, circle2 = self.get_rect_and_circles()

        if isinstance(other, RectCollider2D):
            if rect.colliderect(other.get_rect()):
                return True
            # Vérifier si l’un des cercles touche le rectangle
            for center in [circle1, circle2]:
                closest_x = max(other.get_rect().left, min(center.x, other.get_rect().right))
                closest_y = max(other.get_rect().top, min(center.y, other.get_rect().bottom))
                if center.distance_to(pygame.Vector2(closest_x, closest_y)) < self.radius:
                    return True
            return False

        elif isinstance(other, CircleCollider2D):
            # Vérifier collision avec le rectangle central
            if rect.collidepoint(other.get_center()):
                return True
            # Vérifier collision avec les extrémités
            return any(center.distance_to(other.get_center()) < (self.radius + other.radius)
                       for center in [circle1, circle2])

        elif isinstance(other, CapsuleCollider2D):
            # Simplifié : approximation via bounding box
            my_rect = self.parent.rect
            other_rect = other.parent.rect
            return my_rect.colliderect(other_rect)

        return False
