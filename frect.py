from pygame import Rect, Vector2

class FRect:
    def to_rect(self) -> Rect:
        return Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    @property
    def position(self) -> Vector2:
        return Vector2(self.x, self.y)
    
    @property
    def size(self) -> Vector2:
        return Vector2(self.w, self.h)

    @position.setter
    def position(self, position: Vector2):
        self.x = position.x
        self.y = position.y
    
    @size.setter
    def size(self, size: Vector2):
        self.w = size.x
        self.h = size.y

    def __getitem__(self, key):
        match key:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.w
            case 3:
                return self.h

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.w}, {self.h})"

    def from_vec(position: Vector2, size: Vector2):
        return FRect(position.x, position.y, size.x, size.y)

    def from_rect(rect: Rect):
        return FRect(rect[0], rect[1], rect[2], rect[3])

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h