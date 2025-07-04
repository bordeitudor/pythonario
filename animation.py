from pygame import Rect
import pygame

class Animation:
    def get_frame(self) -> Rect:
        if self.pause:
            return self.last_frame
        if not self.playing:
            return self.frames[0]
        
        if self.last_frame == len(self.frames)-1 and not self.repeat:
            self.playing = False
        elif self.last_frame == len(self.frames)-1:
            self.repeats += 1
        
        self.frame = ((pygame.time.get_ticks() - self._time)// (1000 // self.fps)) % len(self.frames)   
        self.last_frame = self.frame
        return self.frames[self.frame]
    
    def play(self):
        self._time = pygame.time.get_ticks()
        self.playing = True

    def reset(self):
        self.last_frame = 0
        self.playing = False
        self.pause = False
        self.repeats = 0

    def stop(self):
        self.playing = False
    
    def __init__(self, frames: list[Rect], fps: int, repeat: bool = False):
        self.frames = frames
        self.fps = fps
        self.last_frame = 0
        self.playing = False
        self.pause = False
        self.repeat = repeat
        self.repeats = 0
        self._time = 0
        self.frame = 0