import random
from kivy.vector import Vector

class Behavior:
    def __init__(self):
        pass
        
    def update_behavior(self, actor, level_manager, dt):
        pass


class Player(Behavior):
    pass


class Monster(Behavior):
    def update_behavior(self, actor, level_manager, dt):
        if not actor.updated_transform:
            tile_pos = Vector(actor.get_tile_pos())
            tile_pos.x += random.randint(-5,5)
            tile_pos.x = max(0, min(level_manager.num_x-1, tile_pos.x))
            tile_pos.y += random.randint(-5,5)
            tile_pos.y = max(0, min(level_manager.num_y-1, tile_pos.y))
            actor.move_to(level_manager, tile_pos)