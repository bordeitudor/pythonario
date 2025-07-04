from gamestate import GameStateManager
from event_manager import EventManager
from window import Window, event_hook as window_event_hook
import pygame
from pygame import Color, Vector2
from constants import WINDOW_SIZE, WINDOW_TITLE
from sys import stderr
from main_game import MainGame
from level_editor import LevelEditor
from font_manager import FontManager
from surface_manager import SurfaceManager
from input_manager import InputManager, event_hook as input_manager_event_hook
from renderer import Renderer
from camera import Camera

class Engine:
    def run(self):
        self.gamestate_manager.set_state(MainGame())

        while(self.running):
            self.window.clear()
            self.event_manager.update()
            self.gamestate_manager.update()
            self.input_manager.update()
            self.renderer.update()
            self.window.display()
        pass

    def __init__(self):
        
        self.running = False

        pygame.init()

        if not pygame.get_init():
            print("ERROR: Failed to initialize pygame", file=stderr)
            exit(-1)

        self.window = Window(WINDOW_SIZE)
        self.window.title = WINDOW_TITLE
        self.window.background_color = Color(146, 144, 255, 255)

        self.gamestate_manager = GameStateManager()
        self.event_manager = EventManager(window_event_hook, input_manager_event_hook) 
        self.font_manager = FontManager()
        self.surface_manager = SurfaceManager()
        self.input_manager = InputManager()
        self.renderer = Renderer()
        self.camera = Camera(Vector2(0, 0))
        
        self.font_manager.load_font("assets/fonts/super-mario-bros-nes.ttf", "default")
        
        self.surface_manager.load_surface("assets/textures/atlasses/mario.png", "atlas_mario")
        self.surface_manager.load_surface("assets/textures/tilesets/overworld.png", "tileset_overworld")
        self.surface_manager.load_surface("assets/textures/pythonario.png", "sprite_pythonario")
        self.surface_manager.load_surface("assets/textures/atlasses/enemies.png", "atlas_enemies")
        self.surface_manager.load_surface("assets/textures/atlasses/powerups.png", "atlas_powerups")
        
        self.window.icon = self.surface_manager.get_surface("sprite_pythonario")
        
        self.running = True

        pass

instance: Engine