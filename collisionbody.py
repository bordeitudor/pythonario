from pygame import Vector2, Color
from frect import FRect
from drawable import Drawable
from renderrect import RenderRect
from enum import Enum, auto
import pygame
from utils import is_colliding, get_broadphase
from copy import copy

class CollisionSide(Enum):
    Null = auto()
    Top = auto()
    Bottom = auto()
    Left = auto()
    Right = auto()

class CollisionBody(Drawable):
    def draw(self):
        if self.render_broadphase:
            rect = RenderRect(get_broadphase(self.position, self.size, self.old_velocity), self.color, 0, 1)
            rect.draw()
        else:
            rect = RenderRect(FRect(self.position.x, self.position.y, self.size.x, self.size.y), self.color, 0, 1)
            rect.draw()
    
    def update(self) -> None:
        self.position += self.velocity
        self.old_velocity = self.velocity
    
    def is_colliding(self, other):
        return is_colliding(get_broadphase(self.position, self.size, self.velocity), get_broadphase(other.position, other.size, other.velocity))
    
    def solve_collision(self, other, side) -> None:
        match side:
            case CollisionSide.Right:
                self.velocity.x = min(self.velocity.x, 0)
                self.position.x = other.position.x - self.size.x
            case CollisionSide.Left:
                self.velocity.x = max(self.velocity.x, 0)
                self.position.x = other.position.x + other.size.x
            case CollisionSide.Bottom:
                self.velocity.y = min(self.velocity.y, 0)
                self.position.y = other.position.y - self.size.y
            case CollisionSide.Top:
                self.velocity.y = max(self.velocity.y, 0)
                self.position.y = other.position.y + other.size.y
            case CollisionSide.Null:
                return
        
    
    def get_collision_side(self, other) -> CollisionSide:
        if not self.is_colliding(other):
            return CollisionSide.Null
        
        center = self.position + self.size / 2
        other_center = other.position + other.size / 2
        
        diff_x = center.x - other_center.x
        diff_y = center.y - other_center.y
        
        if abs(diff_x) >= abs(diff_y):
            if diff_x <= 0:
                return CollisionSide.Right
            else:
                return CollisionSide.Left
        else:
            if diff_y <= 0:
                return CollisionSide.Bottom
            else:
                return CollisionSide.Top
    
        return CollisionSide.Null
    
    def __init__(self, position: Vector2, size: Vector2, velocity: Vector2 | None = None):
        super().__init__()
        self.position = Vector2(position[0], position[1])
        self.size = Vector2(size[0], size[1])
        self.velocity = Vector2(0, 0) if velocity is None else Vector2(velocity[0], velocity[1])
        self.old_velocity = self.velocity.copy()
        self.color = Color(255, 255, 255, 255)
        self.is_grounded = False
        
        self.render_broadphase = True
        pass