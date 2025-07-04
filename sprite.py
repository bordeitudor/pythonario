from drawable import Drawable
import engine as engine
import pygame
from pygame import Vector2, Surface
from frect import FRect
from copy import copy

class Sprite(Drawable):
    def get_draw_surface(self) -> Surface:
        if not self.surface:
            return None
        if self.size.x < 0 or self.size.y < 0:
            return None
        
        draw_surface = self.surface.subsurface(self.area.to_rect())
        draw_surface = pygame.transform.scale(draw_surface, self.size).convert_alpha()
        
        if self.h_flip == True:
            draw_surface = pygame.transform.flip(draw_surface, True, False)
        if self.v_flip == True:
            draw_surface = pygame.transform.flip(draw_surface, False, True)
        
        draw_surface.set_alpha(self.alpha)
        return draw_surface
    
    def draw(self) -> None:
        surface = self.get_draw_surface()
        if not surface:
            return
        
        position = copy(self.position)
        if not self.ignore_camera:
            position = engine.instance.camera.world_to_screen(position)
        
        engine.instance.window.screen.blit(surface, position)
    
    def __init__(self, surface: Surface, position: Vector2, size : Vector2, area: FRect | None = None):
        super().__init__()
        self.position = copy(position)
        self.size = copy(size)
        self.surface = surface
        if area == None:
            rect = self.surface.get_rect()
            rect = FRect(rect[0], rect[1], rect[2], rect[3])
            self.area = copy(rect)
        else:
            self.area = area
        self.h_flip = False
        self.v_flip = False
        self.alpha = 255