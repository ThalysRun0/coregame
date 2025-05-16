from __future__ import annotations

import pygame
from core.collider2d import *

class Gizmos:
    enabled = True  # Toggle global du mode debug
    alpha = 100     # Niveau de transparence (0 à 255)
    hits_to_draw = []

    @staticmethod
    def toggle():
        Gizmos.enabled = not Gizmos.enabled

    @staticmethod
    def draw_collider(surface, collider: Collider2D, color=(0, 255, 0), width=1):
        if not Gizmos.enabled:
            return

        if isinstance(collider, RectCollider2D):
            Gizmos.draw_rect(surface, collider, color, width)

        elif isinstance(collider, CircleCollider2D):
            Gizmos.draw_circle(surface, collider, color, width)
        
        else:
            raise NotImplementedError(f"Collider type {type(collider)} not supported for Gizmos.")

    @staticmethod
    def draw_rect(surface, rect_collider: RectCollider2D, color, width=1):
        rect = rect_collider.get_rect()
        if width == 0:
            # Filled with alpha
            temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            temp.fill((*color, Gizmos.alpha))
            surface.blit(temp, rect.topleft)
        else:
            pygame.draw.rect(surface, color, rect, width)

    @staticmethod
    def draw_circle(surface, center_collider: CircleCollider2D, color, width=1):
        center = center_collider.get_center()
        radius = center_collider.radius
        if width == 0:
            temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp, (*color, Gizmos.alpha), (radius, radius), radius)
            surface.blit(temp, (center.x - radius, center.y - radius))
        else:
            pygame.draw.circle(surface, color, (int(center.x), int(center.y)), int(radius), width)

    @staticmethod
    def add_hit(hit: Hit, color=(255, 0, 0), normal_scale=20, duration=1.0):
        if DEFAULT_CORE_DEBUG: Debug.main.log(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} -> {hit.other.parent.name} hit {hit.self.parent.name} @(point:{hit.point}, normal:{hit.normal})")
        Gizmos.hits_to_draw.append({
            'hit': hit,
            'color': color,
            'normal_scale': normal_scale,
            'life': duration,
            'max_life': duration,
        })

    @staticmethod
    def update_hit(delta_time: float, data: dict):
        data['life'] -= delta_time
        if data['life'] <= 0:
            Gizmos.hits_to_draw.remove(data)
            return

        data['alpha'] = max(0, int(255 * (data['life'] / data['max_life'])))
        data['color'] = (*data['color'][:3], data['alpha'])
        data['normal_scale'] = data['normal_scale'] * (data['life'] / data['max_life'])

    @staticmethod
    def draw_hit(data: dict, surface: pygame.Surface):
        hit: Hit = data['hit']
        if not hit.collided:
            return

        point = hit.point
        normal = hit.normal
        end = point + normal * data['normal_scale']

        color = (*data['color'][:3], 255)
        pygame.draw.circle(surface, color, (int(point.x), int(point.y)), data['normal_scale'])
        pygame.draw.line(surface, color, point, end, 2)

    @staticmethod
    def update(delta_time: float):
        if not Gizmos.enabled:
            return

        for data in Gizmos.hits_to_draw[:]:
            Gizmos.update_hit(delta_time, data)

    @staticmethod
    def draw(screen: pygame.Surface):
        if not Gizmos.enabled:
            return
        # Surface temporaire avec alpha
        temp_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        for data in Gizmos.hits_to_draw[:]:
            Gizmos.draw_hit(data, temp_surface)

        screen.blit(temp_surface, (0, 0))
