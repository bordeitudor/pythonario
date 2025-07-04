from drawable import Drawable
from collisionbody import CollisionBody, CollisionSide
import pygame
from pygame import Vector2, Color
from drawable import Drawable
from tilemap import Tilemap
from random import choice
from utils import floorvec, is_colliding, get_broadphase
import engine as engine
from frect import FRect
from animation import Animation
from sprite import Sprite

TERMINAL_FALL_SPEED = 6
GRAVITY = 0.25
SPEED = 0.8
JUMP_POWER = 4.5

class Paratroopa(Drawable):
    def draw(self) -> None:
        self.body.size.x = self.sprite.size.x / 1.25
        self.sprite.position.x = self.body.position.x - self.sprite.size.x / 8
        self.sprite.position.y = self.body.position.y + self.body.size.y - self.sprite.size.y
        
        if self.direction == -1:
            self.sprite.h_flip = True
        else:
            self.sprite.h_flip = False
        
        self.sprite.draw()
        
    def update_physics(self):
        if not is_colliding(self.tilemap.get_bounds(), get_broadphase(self.body.position, self.body.size, self.body.velocity)):
            self.delete_flag = 1
            return    

        if self.is_grounded:
            self.body.velocity.y += -JUMP_POWER
        
        self.body.velocity.x = self.direction * SPEED
        self.body.velocity.y += GRAVITY
        self.body.velocity.y = min(self.body.velocity.y, TERMINAL_FALL_SPEED)
        
        next_tile_coord = (self.body.position + self.body.size / 2) + Vector2(self.direction * (self.body.size.x / 2) + self.body.velocity.x, 0)
        next_tile = self.tilemap.constrain(floorvec(self.tilemap.translate(next_tile_coord)))
        next_tile_id = self.tilemap.get_tile(next_tile)
        
        if next_tile_id != -1:
            self.direction = -self.direction

        self.body.color = Color(100, 180, 0, 255)
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
        if not self.walk_animation.playing:
            self.walk_animation.play()
        self.sprite.area = self.walk_animation.get_frame()

    def update(self) -> None:
        self.update_animations()
        self.update_physics()
    
    
    def __init__(self, tilemap: Tilemap):
        super().__init__()
        self.body = CollisionBody(Vector2(0, 0), Vector2(28, 32))
        self.is_grounded = False
        self.tilemap = tilemap
        self.direction = choice([-1,1])
        self.delete_flag = 0
        self.walk_animation = Animation([FRect(35, 1, 16, 24), FRect(52, 1, 16, 24), FRect(35, 1, 16, 24)], 6)
        self.sprite = Sprite(engine.instance.surface_manager.get_surface("atlas_enemies"), self.body.position, Vector2(32, 48), FRect(35, 1, 16, 24))
        self.alive = True
        pass