import inspect
import pygame

from core.constants import *
from core.debug import Debug
from core.gameobject import Gameobject

class Rigidbody2D:
    def __init__(self, parent: Gameobject, mass=1.0, use_gravity=True):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}->parent({parent.name})")
        self.parent = parent
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.mass = mass
        self.use_gravity = use_gravity
        self.gravity = DEFAULT_BODY_GRAVITY
        self.friction = DEFAULT_BODY_FRICTION
        self.inertia = DEFAULT_BODY_INERTIA
        self.on_ground = False

    def apply_gravity(self):
        self.acceleration += self.gravity

    def apply_force(self, force: pygame.Vector2):
        # F = m * a => a = F / m
        self.acceleration += force / self.mass

    def update(self, delta_time):
        if not self.parent.active:
            return
        if self.use_gravity:
            self.apply_gravity()
        effective_acceleration = self.acceleration * (1 - self.inertia)
        self.velocity += effective_acceleration * delta_time
        self.parent.position += self.velocity
        self.acceleration = pygame.Vector2(0, 0)