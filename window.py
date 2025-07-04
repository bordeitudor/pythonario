import pygame
import engine as engine
from pygame import Vector2, Surface, Color
from pygame.event import Event
from utils import tuplevec

class Window:
    def __init__(self, size: Vector2, flags: int = 0, depth: int = 0, display: int = 0, vsync: int = 0):
        self.size = size
        
        self._clock = pygame.time.Clock()
        self._background_color = pygame.Color(0,0,0,255)

    def create(self, size: Vector2 = None, flags: int = None, depth: int = None, vsync: int = None) -> None:
        size = size or self.size
        flags = flags or self.flags
        depth = depth or self.depth
        vsync = vsync or self.vsync
        self._screen = pygame.display.set_mode(size=size,flags=flags,depth=depth,vsync=vsync)
    
    @property
    def vsync(self):
        if not hasattr(self, "_vsync"):
            self._vsync = 0
        return self._vsync

    @property
    def depth(self):
        if not hasattr(self, "_depth"):
            self._depth = 0
        return self._depth

    @property
    def flags(self):
        if not hasattr(self, "_flags"):
            self._flags = 0
        return self._flags

    @property
    def screen(self):
        if not hasattr(self, "_screen"):
            self.create()
        return self._screen

    @property
    def background_color(self):
        if not hasattr(self, "_background_color"):
            self._background_color = Color(0, 0, 0, 255)
        return self._background_color
    
    @background_color.setter
    def background_color(self, color: Color):
        self._background_color = color

    @property
    def max_fps(self):
        if not hasattr(self, "_max_fps"):
            self._max_fps = 60
        return self._max_fps

    @max_fps.setter
    def max_fps(self, max_fps: int) -> None:
        self.max_fps = max_fps

    @property
    def icon(self) -> Surface | None:
        if not hasattr(self, "_icon"):
            self._icon = None
        
        return self._icon

    @icon.setter
    def icon(self, icon: Surface):
        self._icon = icon
        pygame.display.set_icon(icon)

    @property
    def size(self):
        if not hasattr(self, "screen"):
            return Vector2(0, 0)
        
        return tuplevec(self.screen.get_size())

    @size.setter
    def size(self, size: Vector2):
        self._size = size
        self.create()

    @property
    def title(self):
        if not hasattr(self, "_title"):
            self._title = ''
        
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title
        pygame.display.set_caption(title)

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = Vector2(0, 0)
        return self._size

    @size.setter
    def size(self, size: pygame.Vector2) -> pygame.Surface:
        self._size = size
        self.create()

    def clear(self) -> None:
        self.screen.fill(self.background_color)

    def display(self) -> None:
        self._clock.tick(self.max_fps)
        pygame.display.flip()

def event_hook(event: Event) -> None:
    if event.type == pygame.QUIT:
        engine.instance.running = False