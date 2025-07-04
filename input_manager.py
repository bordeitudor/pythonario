

import pygame
import engine as engine
from pygame.event import Event
from pygame import Vector2

STR_TO_KEY = {
    '\b': pygame.K_BACKSPACE,
    '\t': pygame.K_TAB,
    'clear': pygame.K_CLEAR,
    '\n': pygame.K_RETURN,
    'pause': pygame.K_PAUSE,
    'esc': pygame.K_ESCAPE,
    ' ': pygame.K_SPACE,
    '!': pygame.K_EXCLAIM,
    '"': pygame.K_QUOTEDBL,
    '#': pygame.K_HASH,
    '$': pygame.K_DOLLAR,
    '&': pygame.K_AMPERSAND,
    "'": pygame.K_QUOTE,
    '(': pygame.K_LEFTPAREN,
    ')': pygame.K_RIGHTPAREN,
    '*': pygame.K_ASTERISK,
    '+': pygame.K_PLUS,
    ',': pygame.K_COMMA,
    '-': pygame.K_MINUS,
    '.': pygame.K_PERIOD,
    '/': pygame.K_SLASH,
    '0': pygame.K_0,
    '1': pygame.K_1,
    '2': pygame.K_2,
    '3': pygame.K_3,
    '4': pygame.K_4,
    '5': pygame.K_5,
    '6': pygame.K_6,
    '7': pygame.K_7,
    '8': pygame.K_8,
    '9': pygame.K_9,
    ':': pygame.K_COLON,
    ';': pygame.K_SEMICOLON,
    '<': pygame.K_LESS,
    '=': pygame.K_EQUALS,
    '>': pygame.K_GREATER,
    '?': pygame.K_QUESTION,
    '@': pygame.K_AT,
    '[': pygame.K_LEFTBRACKET,
    '\\': pygame.K_BACKSLASH,
    ']': pygame.K_RIGHTBRACKET,
    '^': pygame.K_CARET,
    '_': pygame.K_UNDERSCORE,
    '`': pygame.K_BACKQUOTE,
    'a': pygame.K_a,
    'b': pygame.K_b,
    'c': pygame.K_c,
    'd': pygame.K_d,
    'e': pygame.K_e,
    'f': pygame.K_f,
    'g': pygame.K_g,
    'h': pygame.K_h,
    'i': pygame.K_i,
    'j': pygame.K_j,
    'k': pygame.K_k,
    'l': pygame.K_l,
    'm': pygame.K_m,
    'n': pygame.K_n,
    'o': pygame.K_o,
    'p': pygame.K_p,
    'q': pygame.K_q,
    'r': pygame.K_r,
    's': pygame.K_s,
    't': pygame.K_t,
    'u': pygame.K_u,
    'v': pygame.K_v,
    'w': pygame.K_w,
    'x': pygame.K_x,
    'y': pygame.K_y,
    'z': pygame.K_z,
    'delete': pygame.K_DELETE,
    'kp_0': pygame.K_KP0,
    'kp_1': pygame.K_KP1,
    'kp_2': pygame.K_KP2,
    'kp_3': pygame.K_KP3,
    'kp_4': pygame.K_KP4,
    'kp_5': pygame.K_KP5,
    'kp_6': pygame.K_KP6,
    'kp_7': pygame.K_KP7,
    'kp_8': pygame.K_KP8,
    'kp_9': pygame.K_KP9,
    'kp_.': pygame.K_KP_PERIOD,
    'kp_/': pygame.K_KP_DIVIDE,
    'kp_*': pygame.K_KP_MULTIPLY,
    'kp_-': pygame.K_KP_MINUS,
    'kp_+': pygame.K_KP_PLUS,
    'kp_enter': pygame.K_KP_ENTER,
    'kp_=': pygame.K_KP_EQUALS,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'right': pygame.K_RIGHT,
    'left': pygame.K_LEFT,
    'insert': pygame.K_INSERT,
    'home': pygame.K_HOME,
    'end': pygame.K_END,
    'pageup': pygame.K_PAGEUP,
    'pagedown': pygame.K_PAGEDOWN,
    'f1': pygame.K_F1,
    'f2': pygame.K_F2,
    'f3': pygame.K_F3,
    'f4': pygame.K_F4,
    'f5': pygame.K_F5,
    'f6': pygame.K_F6,
    'f7': pygame.K_F7,
    'f8': pygame.K_F8,
    'f9': pygame.K_F9,
    'f10': pygame.K_F10,
    'f11': pygame.K_F11,
    'f12': pygame.K_F12,
    'f13': pygame.K_F13,
    'f14': pygame.K_F14,
    'f15': pygame.K_F15,
    'numlock': pygame.K_NUMLOCK,
    'capslock': pygame.K_CAPSLOCK,
    'scrollock': pygame.K_SCROLLOCK,
    'rshift': pygame.K_RSHIFT,
    'lshift': pygame.K_LSHIFT,
    'rctrl': pygame.K_RCTRL,
    'lctrl': pygame.K_LCTRL,
    'ralt': pygame.K_RALT,
    'lalt': pygame.K_LALT,
    'rmeta': pygame.K_RMETA,
    'lmeta': pygame.K_LMETA,
    'lsuper': pygame.K_LSUPER,
    'rsuper': pygame.K_RSUPER,
    'mode': pygame.K_MODE,
    'help': pygame.K_HELP,
    'print': pygame.K_PRINT,
    'sysreq': pygame.K_SYSREQ,
    'break': pygame.K_BREAK,
    'menu': pygame.K_MENU,
    'power': pygame.K_POWER,
    'euro': pygame.K_EURO,
    'ac_back': pygame.K_AC_BACK,
}
KEY_TO_STR = {value: key for key, value in STR_TO_KEY.items()}

STR_TO_MOD = {
    'lshift': pygame.KMOD_LSHIFT,
    'rshift': pygame.KMOD_RSHIFT,
    'shift': pygame.KMOD_SHIFT,
    'lctrl': pygame.KMOD_LCTRL,
    'rctrl': pygame.KMOD_RCTRL,
    'ctrl': pygame.KMOD_CTRL,
    'lalt': pygame.KMOD_LALT,
    'ralt': pygame.KMOD_RALT,
    'alt': pygame.KMOD_ALT,
    'lmeta': pygame.KMOD_LMETA,
    'rmeta': pygame.KMOD_RMETA,
    'meta': pygame.KMOD_META,
    'caps': pygame.KMOD_CAPS,
    'num': pygame.KMOD_NUM,
    'mode': pygame.KMOD_MODE
}
MOD_TO_STR = {value: key for key, value in STR_TO_MOD.items()}

STR_TO_MOUSE = {
    'left': 1,
    'middle': 2,
    'right': 3,
    'up': 4,
    'down': 5
}
MOUSE_TO_STR = {value: key for key, value in STR_TO_MOUSE.items()}

class InputManager:
    @property
    def mouse_is_visible(self) -> bool:
        if not hasattr(self, "_mouse_is_visible"):
            self._mouse_is_visible = True
        return self._mouse_is_visible

    @mouse_is_visible.setter
    def mouse_is_visible(self, visible: bool) -> None:
        self._mouse_is_visible = value
    
    @property
    def mouse_pos(self) -> Vector2:
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0], pos[1])
    
    @mouse_pos.setter
    def mouse_pos(self, mouse_pos: Vector2) -> None:
        pygame.mouse.set_pos(mouse_pos)
    
    def is_mouse_released(self, mouse: str) -> bool:
        if mouse not in STR_TO_MOUSE:
            return False
        return not self.is_mouse_pressed(mouse)
    
    def is_mouse_just_released(self, mouse: str) -> bool:
        if mouse not in self.mice_just_released:
            return False
        return self.mice_just_released[mouse]
    
    def is_mouse_just_pressed(self, mouse: str) -> bool:
        if mouse not in self.mice_just_pressed:
            return False
        return self.mice_just_pressed[mouse]
    
    def get_mice_just_released(self) -> list[str]:
        mice = []
        for mouse in self.mice_just_released:
            if self.mice_just_released[mouse]:
                mice.append(mouse)
        return mice
    
    def get_mice_just_pressed(self) -> list[str]:
        mice = []
        for mouse in self.mice_just_pressed:
            if self.mice_just_pressed[mouse]:
                mice.append(mouse)
        return mice
    
    def get_mice_pressed(self) -> list[str]:
        mice = []
        for mouse in self.mice_pressed.keys():
            if self.mice_pressed[mouse]:
                mice.append(mouse)
        return mice
    
    def is_mouse_pressed(self, mouse: str) -> bool:
        if mouse not in STR_TO_MOUSE:
            return False
        return self.mice_pressed[mouse]    
    
    def get_input_key(self) -> str:
        return self._input_key
    
    def get_modifier_keys(self) -> list[str]:
        mods = []
        mod: int = pygame.key.get_mods()
        if mod & pygame.KMOD_LSHIFT:
            mods.append(MOD_TO_STR[pygame.KMOD_LSHIFT])
        if mod & pygame.KMOD_RSHIFT:
            mods.append(MOD_TO_STR[pygame.KMOD_RSHIFT])
        if mod & pygame.KMOD_SHIFT:
            mods.append(MOD_TO_STR[pygame.KMOD_SHIFT])
        if mod & pygame.KMOD_LCTRL:
            mods.append(MOD_TO_STR[pygame.KMOD_LCTRL])
        if mod & pygame.KMOD_RCTRL:
            mods.append(MOD_TO_STR[pygame.KMOD_RCTRL])
        if mod & pygame.KMOD_CTRL:
            mods.append(MOD_TO_STR[pygame.KMOD_CTRL])
        if mod & pygame.KMOD_LALT:
            mods.append(MOD_TO_STR[pygame.KMOD_LALT])
        if mod & pygame.KMOD_RALT:
            mods.append(MOD_TO_STR[pygame.KMOD_RALT])
        if mod & pygame.KMOD_ALT:
            mods.append(MOD_TO_STR[pygame.KMOD_ALT])
        if mod & pygame.KMOD_LMETA:
            mods.append(MOD_TO_STR[pygame.KMOD_LMETA])
        if mod & pygame.KMOD_RMETA:
            mods.append(MOD_TO_STR[pygame.KMOD_RMETA])
        if mod & pygame.KMOD_META:
            mods.append(MOD_TO_STR[pygame.KMOD_META])
        if mod & pygame.KMOD_CAPS:
            mods.append(MOD_TO_STR[pygame.KMOD_CAPS])
        if mod & pygame.KMOD_NUM:
            mods.append(MOD_TO_STR[pygame.KMOD_NUM])
        if mod & pygame.KMOD_MODE:
            mods.append(MOD_TO_STR[pygame.KMOD_MODE])

        return mods
    
    def is_key_released(self, key: str) -> bool:
        if key not in STR_TO_KEY:
            return False
        return not self.is_key_pressed(key)
    
    def is_key_just_released(self, key: str) -> bool:
        if key not in self.keys_just_released:
            return False
        return self.keys_just_released[key]
    
    def is_key_just_pressed(self, key: str) -> bool:
        if key not in self.keys_just_pressed:
            return False
        return self.keys_just_pressed[key]
    
    def get_keys_just_released(self) -> list[str]:
        keys = []
        for key in self.keys_just_released:
            if self.keys_just_released[key]:
                keys.append(key)
        return keys
    
    def get_keys_just_pressed(self) -> list[str]:
        keys = []
        for key in self.keys_just_pressed:
            if self.keys_just_pressed[key]:
                keys.append(key)
        return keys
    
    def get_keys_pressed(self) -> list[str]:
        keys = []
        for key in self.keys_pressed.keys():
            if self.keys_pressed[key]:
                keys.append(key)
        return keys 
    
    def is_key_pressed(self, key: str) -> bool:
        if key not in STR_TO_KEY:
            return False
        keys = pygame.key.get_pressed()
        return keys[STR_TO_KEY[key]]
    
    def update(self):
        for key in self.keys_just_pressed.keys():
                self.keys_just_pressed[key] = False
        
        for key in self.keys_just_released.keys():
                self.keys_just_released[key] = False
        
        for mouse in self.mice_just_pressed.keys():
                self.mice_just_pressed[mouse] = False
        
        for mouse in self.mice_just_released.keys():
                self.mice_just_released[mouse] = False
        
        engine.instance.input_manager._input_key = ''
    
    def __init__(self):
        self.keys_just_pressed = {}
        self.keys_pressed = {}
        self.keys_just_released = {}
        self.mice_just_pressed = {}
        self.mice_pressed = {}
        self.mice_just_released = {}
        self._input_key = ''
        
        for key in STR_TO_KEY.keys():
            self.keys_pressed[key] = False
            self.keys_just_pressed[key] = False
            self.keys_just_released[key] = False
        
        for mouse in STR_TO_MOUSE.keys():
            self.mice_pressed[mouse] = False
            self.mice_just_pressed[mouse] = False
            self.mice_just_released[mouse] = False
        
        pygame.key.set_repeat(200, 70)

def event_hook(event: Event) -> None:
    if event.type == pygame.KEYDOWN:
        if engine.instance.input_manager.keys_pressed[KEY_TO_STR[event.key]] == False:
            engine.instance.input_manager.keys_just_pressed[KEY_TO_STR[event.key]] = True
        engine.instance.input_manager.keys_pressed[KEY_TO_STR[event.key]] = True
        match event.unicode:
            case '\r':
                engine.instance.input_manager._input_key = '\n'
            case _:
                engine.instance.input_manager._input_key = KEY_TO_STR[event.key]
    if event.type == pygame.KEYUP:
        engine.instance.input_manager.keys_pressed[KEY_TO_STR[event.key]] = False
        engine.instance.input_manager.keys_just_released[KEY_TO_STR[event.key]] = True
    if event.type == pygame.MOUSEBUTTONDOWN:
        if engine.instance.input_manager.mice_pressed[MOUSE_TO_STR[event.button]] == False:
            engine.instance.input_manager.mice_pressed[MOUSE_TO_STR[event.button]] = True
        engine.instance.input_manager.mice_pressed[MOUSE_TO_STR[event.button]] = True
    if event.type == pygame.MOUSEBUTTONUP:
        engine.instance.input_manager.mice_pressed[MOUSE_TO_STR[event.button]] = False
        engine.instance.input_manager.mice_just_released[MOUSE_TO_STR[event.button]] = True
        