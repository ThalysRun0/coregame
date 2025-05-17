from __future__ import annotations

import inspect
import pygame
from typing import List, NamedTuple
from abc import ABC, abstractmethod

from core.constants import *
from core.debug import Debug
from core.gameobject import Gameobject

class Hit(NamedTuple):
    collided: bool
    point: pygame.Vector2
    normal: pygame.Vector2
    self: Collider2D
    other: Collider2D


class Hits:
    hits = []

    @staticmethod
    def add_hit(hit: Hit):
        for previous_hit in Hits.hits:
            previous_hit: Hit = previous_hit
            if hit.self == previous_hit.self and hit.other == previous_hit.other:
                return
        Hits.hits.append(hit)
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> Hit[{hit.self.parent.name}, {hit.other.parent.name}, {hit.point}, {hit.normal}]", DEBUG_CORE_INFO)
    
    @staticmethod
    def pop_hit() -> Hit:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> len(Hits.hits:{len(Hits.hits)})", DEBUG_CORE_INFO)
        return Hits.hits.pop(0)

class Collider2D(ABC):
    def __init__(self, parent: Gameobject, is_trigger=False):
        self.parent = parent
        self.is_trigger = is_trigger

    def get_center(self):
        return self.parent.get_center()

    def get_rect(self):
        return self.parent.get_rect()    
    
    def get_circle(self):
        return self.parent.get_circle()

    @abstractmethod
    def get_collision_point(self, other: 'Collider2D') -> pygame.Vector2:
        pass

    @abstractmethod
    def check_collision(self, other: Collider2D) -> Hit:
        pass


class RectCollider2D(Collider2D):
    def __init__(self, parent: Gameobject, is_trigger=False):
        super().__init__(parent, is_trigger)
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> parent({parent.name})", DEBUG_CORE_INFO)
  
    def get_collision_point(self, other: Collider2D) -> pygame.Vector2:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        if isinstance(other, RectCollider2D):
            return self._collide_with_rect(other)
        elif isinstance(other, CircleCollider2D):
            return self._collide_with_circle(other)
        raise NotImplementedError()

    def _collide_with_rect(self, other: 'RectCollider2D') -> pygame.Vector2:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        center = self.get_center()
        rect = other.get_rect()
        closest_x = max(rect.left, min(center.x, rect.right))
        closest_y = max(rect.top, min(center.y, rect.bottom))
        return pygame.Vector2(closest_x, closest_y)

    def _collide_with_circle(self, other: 'CircleCollider2D') -> pygame.Vector2:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        circle_center = other.get_center()
        rect = self.get_rect()
        closest_x = max(rect.left, min(circle_center.x, rect.right))
        closest_y = max(rect.top, min(circle_center.y, rect.bottom))
        return pygame.Vector2(closest_x, closest_y)

    def check_collision(self, other: Collider2D) -> Hit:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        if isinstance(other, RectCollider2D):
            return self._check_rect_rect_collision(other)
        elif isinstance(other, CircleCollider2D):
            return self._check_rect_circle_collision(other)
        raise NotImplementedError()

    def _check_rect_rect_collision(self, other: 'RectCollider2D') -> Hit:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        a = self.get_rect()
        b = other.get_rect()
        collided = a.colliderect(b)
        if not collided:
            return Hit(False, pygame.Vector2(), pygame.Vector2(), self, other)

        # Calcul du point de collision approximatif et de la normale
        point = self.get_collision_point(other)
        center_diff = self.get_center() - other.get_center()
        normal = center_diff.normalize() if center_diff.length_squared() > 0 else pygame.Vector2(1, 1)
        return Hit(True, point, normal, self, other)

    def _check_rect_circle_collision(self, other: 'CircleCollider2D') -> Hit:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        circle_center = other.get_center()
        point = self.get_collision_point(other)
        distance = (circle_center - point).length()
        collided = distance < other.radius
        normal = (circle_center - point).normalize() if collided and distance != 0 else pygame.Vector2(1, 1)
        return Hit(collided, point, normal, self, other)


class CircleCollider2D(Collider2D):
    def __init__(self, parent: Gameobject, radius, is_trigger=False):
        super().__init__(parent, is_trigger)
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> parent({parent.name})", DEBUG_CORE_INFO)
        self.radius = radius
    
    def get_collision_point(self, other: Collider2D) -> pygame.Vector2:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        if isinstance(other, RectCollider2D):
            return other.get_collision_point(self)  # délègue
        elif isinstance(other, CircleCollider2D):
            dir_vector = other.get_center() - self.get_center()
            if dir_vector.length_squared() == 0:
                return self.get_center()
            return self.get_center() + dir_vector.normalize() * self.radius
        raise NotImplementedError()

    def check_collision(self, other: Collider2D) -> Hit:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        if isinstance(other, RectCollider2D):
            return other.check_collision(self)  # délègue
        elif isinstance(other, CircleCollider2D):
            return self._check_circle_circle_collision(other)
        raise NotImplementedError()

    def _check_circle_circle_collision(self, other: 'CircleCollider2D') -> Hit:
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> self({self.parent.name}), other({other.parent.name})", DEBUG_CORE_INFO)
        dir_vector = other.get_center() - self.get_center()
        distance = dir_vector.length()
        collided = distance < (self.radius + other.radius)

        if collided and distance != 0:
            normal = dir_vector.normalize()
            point = self.get_center() + normal * self.radius
        else:
            point = self.get_center()
            normal = pygame.Vector2(1, 1)

        return Hit(collided, point, normal, self, other)