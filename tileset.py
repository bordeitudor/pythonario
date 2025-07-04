from pygame import Surface, Vector2

class Tileset:
    def get_tile(self, id: int) -> Surface:
        
        if not self.is_tile(id):
            return Surface((0,0))

        return self.tiledict[id].copy()
    
    def set_tile(self, id: int, area: tuple[int, int]) -> None:
        self.tiledict[id] = self.surface.subsurface((area[0], area[1], self.tile_size.x, self.tile_size.y)).convert_alpha()
    
    def is_tile(self, id: int) -> bool:
        return id in self.tiledict
    
    def __init__(self, surface: Surface, tile_size: tuple[int, int]):
        self.surface = surface
        self.tile_size = Vector2(tile_size[0], tile_size[1])
        self.tiledict: dict[int, Surface] = {}