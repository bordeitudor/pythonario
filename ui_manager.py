from drawable import Drawable

class UIObject(Drawable):
    def update(self):
        self.children = [child for child in self.children if child]
        for child in self.children:
            child.update()
    
    def add_child(self, uiobject):
        uiobject.parent = self
        self.children.append(uiobject)
    
    def __init__(self):
        self.children: list[UIObject] = []
        self.parent: UIObject = None

class UIManager:
    def update(self):
        assert(self.root)
        self.root.update()
    
    def __init__(self):
        self.root = UIObject()
        pass