from drawable import Drawable
from frect import FRect
import engine as engine
import pygame
from pygame import Color, Surface
from copy import copy

class RenderRect(Drawable):
    def get_draw_surface(self):
        surface = Surface((self.rect.w, self.rect.h))
        surface.set_alpha(self.color.a)
        surface.fill((self.color.r, self.color.g, self.color.b, 255))
        if not self.filled:
            surface.fill((0, 0, 0, 0), rect=(self.outline_thickness, self.outline_thickness, self.rect.w-self.outline_thickness*2, self.rect.h-self.outline_thickness*2))
        return surface
    
    def draw(self):
        surface = self.get_draw_surface()
        position = copy(self.rect.position)
        if not self.ignore_camera:
            position = engine.instance.camera.world_to_screen(position)

        engine.instance.window.screen.blit(surface, position)
    
    def __init__(self, rect: FRect, color: Color, layer: int, outline_thickness: int):
        super().__init__()
        self.color = color
        self.rect = rect
        self.layer = layer
        self.filled = True
        self.outline_thickness = outline_thickness