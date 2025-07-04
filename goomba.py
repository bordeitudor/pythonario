from drawable import Drawable
from collisionbody import CollisionBody, CollisionSide
import pygame
from pygame import Vector2, Color
from drawable import Drawable
from tilemap import Tilemap
from random import choice
from utils import floorvec
import engine as engine
from frect import FRect
from sprite import Sprite
from animation import Animation
from utils import get_broadphase, is_colliding

TERMINAL_FALL_SPEED = 6
GRAVITY = 0.25
SPEED = 0.5
DISAPPEAR_TIME = 450

class Goomba(Drawable):
    def draw(self) -> None:
        self.body.size.y = self.sprite.size.y
        self.body.size.x = self.sprite.size.x / 1.25
        self.sprite.position.x = self.body.position.x - self.sprite.size.x / 8
        self.sprite.position.y = self.body.position.y + self.body.size.y - self.sprite.size.y
        
        if not self.alive and not self.stomped:
            self.sprite.flipped = True
        
        self.sprite.draw()
    
    def update_physics(self):
        if not is_colliding(self.tilemap.get_bounds(), get_broadphase(self.body.position, self.body.size, self.body.velocity)):
            self.delete_flag = 1
            return
        
        if not self.alive and not self.stomped:
            self.body.position.y += TERMINAL_FALL_SPEED
            return
        
        if not self.alive and self.stomped:
            self.time_since_death = pygame.time.get_ticks() - self.time_of_death
            self.delete_flag = self.time_since_death > DISAPPEAR_TIME
            return
        
        self.body.velocity.x = self.direction * SPEED
        self.body.velocity.y += GRAVITY
        self.body.velocity.y = min(self.body.velocity.y, TERMINAL_FALL_SPEED)

        next_lower_tile_coord = (self.body.position + self.body.size / 2) + Vector2(self.direction * (self.body.size.x / 2) + self.body.velocity.x, self.body.size.y / 2)
        next_lower_tile = self.tilemap.constrain(floorvec(self.tilemap.translate(next_lower_tile_coord)))
        next_lower_tile_id = self.tilemap.get_tile(next_lower_tile)
        
        next_tile_coord = (self.body.position + self.body.size / 2) + Vector2(self.direction * (self.body.size.x / 2) + self.body.velocity.x, 0)
        next_tile = self.tilemap.constrain(floorvec(self.tilemap.translate(next_tile_coord)))
        next_tile_id = self.tilemap.get_tile(next_tile)
        
        if next_lower_tile_id == -1 or next_tile_id != -1:
            self.direction = -self.direction

        self.body.color = Color(150, 75, 0, 255)
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
        if not self.alive and self.stomped:
            self.sprite.area = FRect(35, 51, 16, 16)
            return
        elif not self.alive and not self.stomped:
            self.sprite.area = FRect(1, 51, 16, 16)
        if not self.walk_animation.playing and self.alive:
            self.walk_animation.play()
        self.sprite.area = self.walk_animation.get_frame()
    
    def update(self) -> None:
        self.update_animations()
        self.update_physics()
    
    def stomp(self):
        self.alive = False
        self.time_since_death = 0
        self.time_of_death = pygame.time.get_ticks()
        self.stomped = True
    
    def kill(self):
        self.alive = False
        self.stomped = False
        self.sprite.v_flip = True
        self.walk_animation.stop()
    
    def __init__(self, tilemap: Tilemap):
        super().__init__()
        self.alive = True
        self.body = CollisionBody(Vector2(0, 0), Vector2(28, 32))
        self.is_grounded = False
        self.tilemap = tilemap
        self.direction = choice([-1,1])
        self.time_since_death = 0
        self.time_of_death = 0
        self.delete_flag = 0
        self.stomped = False
        self.walk_animation = Animation([FRect(1, 51, 16, 16), FRect(18, 51, 16, 16), FRect(1, 51, 16, 16)], 4)
        self.sprite = Sprite(engine.instance.surface_manager.get_surface("atlas_enemies"), self.body.position, Vector2(32, 32), FRect(1, 51, 16, 16))
        pass