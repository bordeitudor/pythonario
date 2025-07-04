import pygame

class EventManager:
    def __init__(self, *hooks):
        self.hooks = list(hooks)
    
    def update(self):
        for event in pygame.event.get():
            for hook in self.hooks:
                hook(event)