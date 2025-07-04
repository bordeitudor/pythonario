import os
import pygame
from sys import stderr
from utils import clamp

class FontManager:   
    def get_font(self, font_name: str, font_size: int) -> pygame.font.Font | None:
        if font_name not in self.fonts:
            return None
        if font_size not in self.fonts[font_name]:
            listrange = list(self.FONT_SIZE_RANGE)
            font_size = clamp(font_size, listrange[0], listrange[1])
        return self.fonts[font_name][font_size]

    def load_sysfont(self, font_name: str) -> None:
        if font_name not in pygame.font.get_fonts():
            print(f"ERROR: Failed to load sysfont: No such font `{font_name}`", file=stderr)
            exit(-1)

        for i in self.FONT_SIZE_RANGE:
            self.fonts[font_name][i] = pygame.font.SysFont(font_name, i)
    
    def load_font(self, font_path: str, font_name: str) -> None:
        if not os.path.exists(font_path):
            print(f"ERROR: Failed to load font: No such file or directory `{font_name}`")
            exit(-1)

        if font_name not in self.fonts:
            self.fonts[font_name] = {}

        for i in self.FONT_SIZE_RANGE:
            self.fonts[font_name][i] = pygame.font.Font(font_path, i)

    def __init__(self):
        self.fonts: dict[str, dict[int, pygame.font.Font]] = {}
        pass
    
    FONT_SIZE_RANGE = range(1, 72)