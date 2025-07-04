from copy import copy

class GameState:
    def __init__(self):
        pass

    def init(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class GameStateManager:

    def __init__(self):
        self.bufferstate = None
        pass

    def set_state(self, state) -> None:
        self.bufferstate = copy(state)
    
    def get_state() -> GameState:
        return self.state
    
    def update(self):
        if self.bufferstate != None:
            self.state = self.bufferstate
            self.bufferstate = None
            self.state.init()
        
        self.state.draw()
        self.state.update()