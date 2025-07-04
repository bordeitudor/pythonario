from drawable import Drawable
from sprite import Sprite
from pygame import Vector2, Rect, Surface
from utils import clamp, tuplevec
from tileset import Tileset
from sprite import Sprite
from math import floor, ceil
from collisionbody import CollisionBody, get_broadphase
from frect import FRect
from copy import copy
import engine as engine

class Tilemap(Drawable):
    def get_bounds(self) -> FRect:
        x = 0
        y = 0
        w = (self.size[0]-1) * self.tile_size
        h = (self.size[1]-1) * self.tile_size
        return FRect(x, y, w, h)
    
    def constrain(self, pos: Vector2) -> Vector2:
        return Vector2(
            clamp(int(pos[0]), 0, self.size[0] - 1),
            clamp(int(pos[1]), 0, self.size[1] - 1)
        )
    
    def get_body_bounds(self, body: CollisionBody) -> Rect:
        bp = get_broadphase(body.position, body.size, body.velocity)
        position = bp.position
        size = bp.size
        
        p1 = self.translate(position)
        p2 = self.translate(position + size)
        
        p1[0] = clamp(floor(p1[0]), 0, self.size[0])
        p1[1] = clamp(floor(p1[1]), 0, self.size[1])
        
        p2[0] = clamp(ceil(p2[0]), 0, self.size[0])
        p2[1] = clamp(ceil(p2[1]), 0, self.size[1])
        
        rect = Rect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1])
        return rect
    
    def get_tile_collision_body(self, pos: Vector2) -> CollisionBody:
        if self.get_tile(pos) is None:
            return None
        
        x = int(pos[0]) * self.tile_size
        y = int(pos[1]) * self.tile_size
        position = Vector2(x, y)
        size = Vector2(self.tile_size, self.tile_size)
        return CollisionBody(position, size, (0,0))
    
    def get_tile(self, pos: Vector2) -> int:
        if not int(pos[0]) in range(0, int(self.size[0])) or not int(pos[1]) in range(0, int(self.size[1])):
            return None
        
        return self.tiles[int(pos[0])][int(pos[1])]
    
    def translate_back(self, position: Vector2) -> Vector2:
        result = Vector2(
            position.x * self.tile_size,
            position.y * self.tile_size
        )
        return result
    
    def translatef(self, x: float) -> Vector2:
        return x / self.tile_size
    
    def translate(self, position: Vector2) -> Vector2:
        result = Vector2(
            self.translatef(position.x),
            self.translatef(position.y)
        )
        return result
    
    def draw(self):
        surface = self.get_draw_surface()
        if not surface:
            return
        
        position = engine.instance.camera.world_to_screen(Vector2(0,0))
        engine.instance.window.screen.blit(surface, position)
    
    def get_draw_surface(self) -> None:
        surface = Surface((self.size.x, self.size.y)).convert_alpha()
        
        visible = FRect(0,0,0,0)
        visible.x = int(self.translatef(floor(engine.instance.camera.center.x - engine.instance.window.size.x / 2)))
        visible.y = int(self.translatef(floor(engine.instance.camera.center.y - engine.instance.window.size.y / 2)))
        visible.w = int(self.translatef(ceil(engine.instance.camera.center.x - engine.instance.window.size.x / 2 + engine.instance.window.size.x)))+1
        visible.h = int(self.translatef(ceil(engine.instance.camera.center.y - engine.instance.window.size.y / 2 + engine.instance.window.size.y)))+1
        
        visible.position = self.constrain(visible.position)
        visible.size = self.constrain(visible.size)
        
        if visible.x < 0 or visible.x >= self.size[0]:
            return None
        if visible.y < 0 or visible.y >= self.size[1]:
            return None
        if visible.w < 0 or visible.w >= self.size[0]:
            return None
        if visible.h < 0 or visible.h >= self.size[1]:
            return None        
        result = Surface(((visible.w) * self.tile_size, (visible.h) * self.tile_size)).convert_alpha()
        result.fill((0, 0, 0, 10))
    
        
        for i in range(int(visible.x), int(visible.w)):
            for j in range(int(visible.y), int(visible.h)):
                
                tile = self.tiles[i][j]
                if tile == -1:
                    continue
                
                position = (i * self.tile_size, j * self.tile_size)
                
                surface = self.tileset.get_tile(tile)
                size = self.tile_size
                sprite = Sprite(surface, position, Vector2(size, size), FRect.from_rect(surface.get_rect()))
                sprite_surface = sprite.get_draw_surface()
                result.blit(sprite_surface, (i * self.tile_size,j * self.tile_size))
        return result
    
    def __init__(self, size: Vector2, tile_size: int, tileset: Tileset):
        super().__init__()
        self.tiles = [[-1] * int(size[1]) for _ in range(int(size[0]))]
        self.size = copy(size)
        self.tileset = tileset
        self.tile_size = copy(tile_size)