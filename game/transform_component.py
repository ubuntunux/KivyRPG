from kivy.logger import Logger
from kivy.vector import Vector
from utility.kivy_helper import *
from .constant import *
from .. import main

class TransformComponent():
    def __init__(self, pos):
        pos = get_discrete_center(pos, TILE_SIZE)
        self.pos = Vector(pos)
        self.walk_speed = 1000.0
        self.target_positions = []
        self.is_1d_type = True
        self.logger = main.KivyRPGApp.instance()
        
    def get_pos(self):
        return self.pos
        
    def move_to(self, target_pos):
        target_pos = Vector(get_discrete_center(target_pos, TILE_SIZE))
        if target_pos != self.pos:
            self.target_positions = [Vector(target_pos)]
            if self.is_1d_type:
                tile_pos = Vector(get_discrete_center(self.pos, TILE_SIZE))
                to_tile = (tile_pos - self.pos)
                is_vertical_line = (to_tile.x == 0.0)
                to_target = (target_pos - tile_pos)
                is_origin = (tile_pos == self.pos)
                if is_vertical_line or abs(to_target.x) <= abs(to_target.y):
                    target_pos.x = tile_pos.x
                else:
                    target_pos.y = tile_pos.y
                self.target_positions.append(target_pos)        
        
    def update_transform(self, dt):
        if self.target_positions:
            target_pos = self.target_positions[-1]
            to_target = (target_pos - self.pos).normalize()
            move_dist = self.walk_speed * dt
            dist = target_pos.distance(self.pos)
            if dist <= move_dist:
                self.pos = target_pos
                self.target_positions.pop()
            else:
                self.pos = self.pos + to_target * move_dist
            return True
        return False