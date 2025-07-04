from gamestate import GameState, GameStateManager
from collisionbody import CollisionBody, CollisionSide, get_broadphase
from pygame import Vector2, Rect, Color
import pygame
import engine as engine
from sprite import Sprite
from tileset import Tileset
from tilemap import Tilemap
from mario import Mario, COYOTE_TIME_MAX, DeadMario, PowerupState
from utils import clamp
from math import ceil, floor
from goomba import Goomba
from green_koopa import GreenKoopa
from green_koopa_shell import GreenKoopaShell
from paratroopa import Paratroopa
import green_koopa_shell
import red_koopa_shell
from red_koopa_shell import RedKoopaShell
from red_koopa import RedKoopa
from world import World
from animation import Animation
from copy import copy
import constants
from mushroom import Mushroom
from fire_flower import FireFlower

class MainGame(GameState):
    def update(self):
        engine.instance.camera.center = copy(self.world.mario.body.position)
        engine.instance.camera.center.x = clamp(engine.instance.camera.center.x, engine.instance.window.size.x/2, self.world.tilemap.get_bounds().w - engine.instance.window.size.x / 2)
        engine.instance.camera.center.y = self.world.tilemap.get_bounds().h - engine.instance.window.size.y / 2
        
        buttons = engine.instance.input_manager.get_mice_pressed()
        mpos = engine.instance.camera.screen_to_world(engine.instance.input_manager.mouse_pos)
        if 'left' in buttons:
            coords = self.world.tilemap.constrain(self.world.tilemap.translate(mpos))
            coords = Vector2(floor(coords[0]), floor(coords[1]))
            self.world.tilemap.tiles[int(coords[0])][int(coords[1])] = 0
        elif 'right' in buttons:
            coords = self.world.tilemap.constrain(self.world.tilemap.translate(mpos))
            coords = Vector2(floor(coords[0]), floor(coords[1]))
            self.world.tilemap.tiles[int(coords[0])][int(coords[1])] = -1
        
        if engine.instance.input_manager.is_key_just_pressed('k'):
            green_koopa = GreenKoopa(self.world.tilemap)
            green_koopa.body.position = mpos
            self.world.green_koopas.append(green_koopa)
        
        if engine.instance.input_manager.is_key_just_pressed('r'):
            red_koopa = RedKoopa(self.world.tilemap)
            red_koopa.body.position = mpos
            self.world.red_koopas.append(red_koopa)
        
        if engine.instance.input_manager.is_key_just_pressed('p'):
            paratroopa = Paratroopa(self.world.tilemap)
            paratroopa.body.position = mpos
            self.world.paratroopas.append(paratroopa)
        
        if engine.instance.input_manager.is_key_just_pressed('g'):
            goomba = Goomba(self.world.tilemap)
            goomba.body.position = mpos
            self.world.goombas.append(goomba)
        
        if engine.instance.input_manager.is_key_just_pressed('r'):
            koopa = RedKoopa(self.world.tilemap)
            koopa.body.position = mpos
            self.world.red_koopas.append(koopa)
        
        if engine.instance.input_manager.is_key_just_pressed('m'):
            mushroom = Mushroom(self.world.tilemap)
            mushroom.body.position = mpos
            self.world.mushrooms.append(mushroom)
        
        if engine.instance.input_manager.is_key_just_pressed('f'):
            flower = FireFlower(self.world.tilemap)
            flower.body.position = mpos
            self.world.fire_flowers.append(flower)
            
        
        self.world.update()
        self.world.mario.body.position.x = clamp(self.world.mario.body.position.x, 0, self.world.tilemap.get_bounds().w - self.world.mario.body.size.x)
    
    def init(self):
        
        self.world = World()
        
        tileset_surface = engine.instance.surface_manager.get_surface("tileset_overworld")
        self.world.tileset = Tileset(tileset_surface, (16,16))
        
        tile_count = 0
        for i in range(8):
            for j in range(4):
                x = (i * 16) + 1
                y = (j * 16) + 1
                
                self.world.tileset.set_tile(tile_count, (x,y))
                tile_count += 1
        
        self.world.tilemap = Tilemap(Vector2(64,16), constants.TILE_SIZE, self.world.tileset)
        for i in range(int(self.world.tilemap.size.x)):
            self.world.tilemap.tiles[i][8] = 0
    
        self.world.mario = Mario(self.world)
        self.world.mario.powerup_state = PowerupState.Small
        self.world.mario.body.render_broadphase = False
        self.world.dead_mario = None
    
    def draw(self):
        self.world.draw()