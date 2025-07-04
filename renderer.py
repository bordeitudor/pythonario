from drawable import Drawable

class Renderer:
    def draw(self, drawable):
        obj = drawable
        self.calls.append(obj)
    
    def update(self):
        self.calls.sort(key=lambda x: x.layer, reverse=True)
        for call in self.calls:
            call.draw()
        self.calls = []
    
    def __init__(self):
        self.calls = []
        pass