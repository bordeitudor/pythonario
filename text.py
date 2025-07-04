import pygame
from drawable import Drawable
import engine as engine
from pygame import Vector2, Surface, Color
from utils import clamp

class Text(Drawable):
    def __init__(self, text: str, color: Color, font_name: str, font_size: int):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.color = color
        self.position = Vector2(0, 0)
        self.use_aa = False
        self.font = None
        self.set_font_name(font_name)
        self.set_font_size(font_size)
        self.surface = None
        self._render_text()
    
    def get_lines(self):
        return self.text.split("\n")
            
    def insert_char(self, char: str, idx: int = -1):
        if char == '':
            return
        idx = len(self.text) if idx == -1 else idx
        strtext = list(self.text)
        strtext.insert(idx, char)
        text = ''.join(strtext)
        self.set_text(text)
    
    def set_text(self, new_text: str):
        i = 0
        while True:
            if i >= len(new_text):
                break
            
            if new_text[i] == '\b':
                new_text = list(new_text)
                del new_text[i]
                if i-1 > -1:
                    del new_text[i-1]
                new_text = ''.join(new_text)
                i -= 1
            
            i += 1
        
        self.text = new_text
        self._render_text()

    def set_font_name(self, font_name: str) -> None:
        self.font_name = font_name
        self.font = engine.instance.font_manager.get_font(self.font_name, self.font_size)
        self._render_text()

    def set_font_size(self, font_size: int) -> None:
        self.font_size = font_size
        self.font = engine.instance.font_manager.get_font(self.font_name, self.font_size)
        self._render_text()

    def _render_text(self) -> None:
        text = self.get_lines()
        surfaces = []
        self.size = Vector2(0, 0)
        for line in text:
            surface = self.font.render(line, self.use_aa, self.color).convert_alpha()
            surfaces.append(surface)
            surface_size = surface.get_size()
            surface_size = Vector2(surface_size[0], surface_size[1])
            if surface_size.x > self.size.x:
                self.size.x = surface_size.x
            self.size.y += surface_size.x
        
        self.surface = Surface((int(self.size.x), int(self.size.y))).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        
        y_offset = 0
        for surface in surfaces:
            self.surface.blit(surface, Vector2(0, y_offset))
            y_offset += surface.get_size()[1]
    def draw(self) -> None:
        if self.surface == None:
            return
        engine.instance.window.screen.blit(self.surface, self.position)