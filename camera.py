from pygame import Vector2
import engine as engine

class Camera:
    def world_to_screen(self, position: Vector2) -> Vector2:
        return position - self.center + engine.instance.window.size / 2
    
    def screen_to_world(self, position: Vector2) -> Vector2:
        return position + self.center - engine.instance.window.size / 2
    
    def __init__(self, center: Vector2):
        self.center = center
        pass