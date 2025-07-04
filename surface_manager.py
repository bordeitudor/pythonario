import pygame
import os
import sys

class SurfaceManager:
    def get_surface(self, surface_name: str) -> pygame.Surface | None:
        if surface_name not in self.surfaces:
            return None
        return self.surfaces[surface_name]
    
    def load_surface(self, surface_path: str, surface_name: str) -> None:
        
        if not os.path.exists(surface_path):
            print(f"ERROR: Failed to load surface: No such file or directory `{surface_path}`", file=stderr)
            exit(-1)
        
        self.surfaces[surface_name] = pygame.image.load(surface_path)
    
    def __init__(self):
        self.surfaces: dict[str, pygame.Surface] = {}