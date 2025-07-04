from drawable import Drawable
from collisionbody import CollisionBody, CollisionSide
import pygame
from pygame import Vector2, Color
from drawable import Drawable
from tilemap import Tilemap
from random import choice
from utils import floorvec, is_colliding, get_broadphase
from sprite import Sprite
import engine as engine
from frect import FRect
from animation import Animation

TERMINAL_FALL_SPEED = 6
GRAVITY = 0.25

class FireFlower(Drawable):
    def draw(self) -> None:
        self.body.size.x = self.sprite.size.x / 1.25
        self.sprite.position.x = self.body.position.x - self.sprite.size.x / 8
        self.sprite.position.y = self.body.position.y + self.body.size.y - self.sprite.size.y
        
        self.sprite.draw()
        
    def update_physics(self) -> None:
        if not is_colliding(self.tilemap.get_bounds(), get_broadphase(self.body.position, self.body.size, self.body.velocity)):
            self.delete_flag = 1
            return
        
        self.body.velocity.y += GRAVITY
        self.body.velocity.y = min(self.body.velocity.y, TERMINAL_FALL_SPEED)
        
        self.body.color = Color(250, 150, 100, 255)
        rect = self.tilemap.get_body_bounds(self.body)
        
        self.is_grounded = False
        tiles_collided_with = []
        for x in range(rect[0], rect[0] + rect[2]):
            for y in range(rect[1], rect[1] + rect[3]):
                tile = self.tilemap.tiles[x][y]
                
                if tile != -1:
                    tile_body = self.tilemap.get_tile_collision_body((x,y))
                    tiles_collided_with.append(tile_body)
        
        tiles_collided_with.sort(key = lambda tile: (tile.position + tile.size / 2).distance_to(self.body.position + self.body.size / 2))
        for tile in tiles_collided_with:
            side = self.body.get_collision_side(tile)
            self.body.solve_collision(tile, side)
            if side == CollisionSide.Bottom:
                self.is_grounded = True
        
        self.body.update()
    
    def update_animations(self):
        if not self.animation.playing:
            self.animation.play()
        self.sprite.area = self.animation.get_frame()
    
    def update(self):
        self.update_animations()
        self.update_physics()
    
    def __init__(self, tilemap: Tilemap):
        super().__init__()
        self.body = CollisionBody(Vector2(0, 0), Vector2(28, 32))
        self.sprite = Sprite(engine.instance.surface_manager.get_surface("atlas_powerups"), self.body.position, Vector2(32,32), FRect(18,1,16,16))
        self.animation = Animation([FRect(18, 1, 16, 16), FRect(35, 1, 16, 16), FRect(52, 1, 16, 16), FRect(69, 1, 16, 16)], 50)
        self.is_grounded = False
        self.tilemap = tilemap
        self.direction = choice([-1,1])
        self.delete_flag = 0
        pass