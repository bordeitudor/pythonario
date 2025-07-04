from gamestate import GameState
from text import Text
import engine as engine
from pygame import Vector2, Color, Surface
import pygame
from tileset import Tileset
from utils import clamp, is_colliding, get_broadphase, tuplevec, tuplefrect
from sprite import Sprite
from textedit import TextEdit
from frect import FRect
from math import floor
from tilemap import Tilemap
from copy import copy
from renderrect import RenderRect
import constants

CAMERA_SPEED = 4

class LevelEditor(GameState):
    def draw(self):
        tile_picker_sprites = self.tile_picker_sprites[self.tile_picker_idx:]
        for i in range(len(tile_picker_sprites)):
            if i >= self.num_tile_picker_tiles_to_render:
                break
            sprite = tile_picker_sprites[i][0]
            engine.instance.renderer.draw(sprite)
        engine.instance.renderer.draw(self.text)
        engine.instance.renderer.draw(self.tilemap)
        engine.instance.renderer.draw(self.tile_picker_rect)
        
        self.draw_ghost_tile()

    def update(self):
        self.just_selected_tile = False
        
        if engine.instance.input_manager.is_key_pressed('left'):
            engine.instance.camera.center.x -= CAMERA_SPEED
        elif engine.instance.input_manager.is_key_pressed('right'):
            engine.instance.camera.center.x += CAMERA_SPEED
        
        if engine.instance.input_manager.is_key_pressed('up'):
            engine.instance.camera.center.y -= CAMERA_SPEED
        elif engine.instance.input_manager.is_key_pressed('down'):
            engine.instance.camera.center.y += CAMERA_SPEED
        
        self.handle_tile_picking()
        self.handle_tile_placement()
        
    def handle_tile_picking(self):
        if engine.instance.input_manager.is_key_just_pressed('q'):
            self.tile_picker_idx = max(self.tile_picker_idx-1, 0)
        elif engine.instance.input_manager.is_key_just_pressed('e'):
            self.tile_picker_idx += 1
            if len(self.tiles)-self.tile_picker_idx < self.num_tile_picker_tiles_to_render:
                self.tile_picker_idx -= 1

        tile_picker_sprites = self.tile_picker_sprites[self.tile_picker_idx:]
        for i in range(len(tile_picker_sprites)):
            if i >= self.num_tile_picker_tiles_to_render:
                break
            
            sprite = tile_picker_sprites[i][0]
            sprite.position.x = self.tile_picker_offset + i * self.tile_size
            
            buttons = engine.instance.input_manager.get_mice_pressed()
            if 'left' in buttons:
                mouse_pos = engine.instance.input_manager.mouse_pos
                mouse_rect = FRect(mouse_pos.x, mouse_pos.y, 1, 1)
                sprite_rect = FRect(sprite.position.x, sprite.position.y, sprite.size.x, sprite.size.y)
                if is_colliding(mouse_rect, sprite_rect):
                    tile = tile_picker_sprites[i][1]
                    self.selected_tile = tile
                    self.just_selected_tile = True
                    self.selected_tile_sprite = copy(sprite)
        
    def handle_tile_placement(self):
        buttons = engine.instance.input_manager.get_mice_pressed()
        mpos = engine.instance.input_manager.mouse_pos
        mpos = engine.instance.camera.screen_to_world(mpos)

        coords = self.tilemap.constrain(self.tilemap.translate(mpos))
        coords = Vector2(floor(coords[0]), floor(coords[1]))
    
        
        if 'left' in buttons and not self.just_selected_tile:
            self.tilemap.tiles[int(coords[0])][int(coords[1])] = self.selected_tile
        elif 'right' in buttons and not self.just_selected_tile:
            self.tilemap.tiles[int(coords[0])][int(coords[1])] = -1
            
    def draw_ghost_tile(self):
        mpos = engine.instance.input_manager.mouse_pos
        mpos = engine.instance.camera.screen_to_world(mpos)

        coords = self.tilemap.constrain(self.tilemap.translate(mpos))
        coords = Vector2(floor(coords[0]), floor(coords[1]))
        
        if self.selected_tile != -1 and self.selected_tile_sprite != None:
            self.selected_tile_sprite.position = engine.instance.camera.world_to_screen(self.tilemap.translate_back(coords))
            self.selected_tile_sprite.layer = -98
            self.selected_tile_sprite.alpha = 150
            engine.instance.renderer.draw(self.selected_tile_sprite)
    
    def regen_tiles(self):
        self.tile_picker_sprites = []
        for tile in self.tiles:
            y = (7.5/8) * engine.instance.window.size.y
            x = self.tile_picker_offset + self.tile_size*tile
            
            sprite = Sprite(self.tileset.get_tile(tile), Vector2(x,y), Vector2(32,32), FRect(0, 0, 16, 16))
            sprite.layer = -1000
            sprite.ignore_camera = True
            self.tile_picker_sprites.append((sprite, tile))
    
    def init(self):
        self.text = Text("LEVEL EDITOR", (255, 255, 255, 255), "default", 14)
        self.tileset = Tileset(engine.instance.surface_manager.get_surface("tileset_overworld"), Vector2(16,16))
        self.tilemap = Tilemap(Vector2(16,16), constants.TILE_SIZE, self.tileset)
        self.tilemap.layer = -100
        self.tiles = []
        
        self.text.layer = -1000
        
        self.tile_picker_rect = RenderRect(FRect(0, (7.4/8) * engine.instance.window.size.y, engine.instance.window.size.x, engine.instance.window.size.y), Color(20, 20, 20, 150), -99)
        self.tile_picker_rect.layer = -999
        self.tile_picker_rect.ignore_camera = True
        self.tile_picker_sprites = []
        self.tile_picker_idx = 0
        self.tile_size = 32
        self.tile_picker_offset = self.tile_size
        self.tile_picker_width = engine.instance.window.size.x - self.tile_picker_offset
        self.num_tile_picker_tiles_to_render = int(self.tile_picker_width // self.tile_size)-1
        self.selected_tile = 0
        self.just_selected_tile = False
        self.selected_tile_sprite = None
        
        i = 0
        for k in range(0, 4):
            for j in range(0, 8):
                x = (j * 16) + j+1
                y = (k * 16) + k+1
                self.tileset.set_tile(i, Vector2(x,y))
                self.tiles.append(i)
                i += 1
        del i
        self.regen_tiles()
    