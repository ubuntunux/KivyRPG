from kivy.vector import Vector

TILE_WIDTH = 128
TILE_HEIGHT = TILE_WIDTH
TILE_SIZE = Vector(TILE_WIDTH, TILE_HEIGHT)

def pos_to_tile(pos):
    tile_pos = Vector(pos) / TILE_SIZE
    tile_pos.x = int(tile_pos.x)
    tile_pos.y = int(tile_pos.y)
    return tile_pos
    
def tile_to_pos(tile_pos):
    pos = Vector(tile_pos) * TILE_SIZE
    pos.x += TILE_WIDTH * 0.5
    pos.y += TILE_HEIGHT * 0.5
    return pos