from ui_manager import UIObject
from pygame import Color, Vector2
from text import Text
import engine as engine
from drawable import Drawable
from utils import clamp
from renderrect import RenderRect
from frect import FRect

class TextEdit(Drawable):
    def draw(self):
        self.text.draw()

        lines = self.text.get_lines()
        newlines = len([char for char in self.text.text[:self.idx] if char == '\n'])
                
        text = lines[newlines]
        
        lastnewline = self.text.text[:self.idx].rfind("\n")
        
        true_idx = self.idx - lastnewline - 1
        
        text_size = self.text.font.render(text[:true_idx], self.text.font_size, (0,0,0,0)).get_size()
        text_size = Vector2(text_size[0], text_size[1])
        cursor_pos = self.position
        
        x = cursor_pos[0] + text_size[0]
        y = cursor_pos[1] + text_size[1] * newlines
        w = 2
        h = text_size[1]
        
        position = Vector2(x,y)
        
        if not self.ignore_camera:
            position = engine.instance.world_to_screen(position)
        
        size = Vector2(w, h)
    
        rect = RenderRect(FRect(position.x, position.y, size.x, size.y), (255, 255, 255, 255), self.layer-1)
        rect.draw()
    
    def update(self):
        self.text.position = self.position
        self.text.layer = self.layer
        
        key = engine.instance.input_manager.get_input_key()
        
        if len(key) == 1:
            if ord(key) == 10 and not self.multiple_lines:
                return
            
            self.text.insert_char(key, self.idx)
            if ord(key) == 8:
                self.idx = clamp(self.idx-1, 0, len(self.text.text))
            else:
                self.idx = clamp(self.idx+1, 0, len(self.text.text))
        elif key == 'left':
            self.idx = clamp(self.idx-1, 0, len(self.text.text))
        elif key == 'right':
            self.idx = clamp(self.idx+1, 0, len(self.text.text))
    
    def __init__(self, text: str, color: Color, font_name: str, font_size: int):
        super().__init__()
        self.text = Text(text, color, font_name, font_size)
        self.idx = len(self.text.text)
        self.position = Vector2(0, 0)
        self.multiple_lines = False
        pass