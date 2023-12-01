from kivy.logger import Logger
from kivy.vector import Vector
from utility.kivy_helper import *
from .constant import *
from .. import main

class TransformComponent():
    def __init__(self, actor, tile_pos):
        self.actor = actor
        self.tile_pos = Vector(tile_pos)
        self.pos = tile_to_pos(tile_pos)
        self.front = Vector(1, 0)
        self.target_positions = []
        self.grid_based_movement = True
        self.logger = main.KivyRPGApp.instance()
        # properties
        self.walk_speed = 1000.0
        
    def get_pos(self):
        return self.pos
        
    def get_tile_pos(self):
        return self.tile_pos
           
    def move_to(self, target_tile_pos):
        target_pos = tile_to_pos(target_tile_pos)
        self.target_positions = [Vector(target_pos)]
        if self.grid_based_movement:
            tile_world_pos = tile_to_pos(self.tile_pos)
            to_tile = (tile_world_pos - self.pos)
            is_vertical_line = (to_tile.y != 0.0 and to_tile.x == 0.0)
            is_origin = (tile_world_pos == self.pos)
            to_target = (target_pos - tile_world_pos)
            if is_vertical_line or abs(to_target.x) <= abs(to_target.y):
                target_pos.x = tile_world_pos.x
            else:
                target_pos.y = tile_world_pos.y
            self.target_positions.append(target_pos)        
        
    def update_transform(self, level_manager, dt):
        if self.target_positions:
            # calc target pos
            target_pos = self.target_positions[-1]
            to_target = (target_pos - self.pos).normalize()
            move_dist = self.walk_speed * dt
            dist = target_pos.distance(self.pos)
            # calc next pos
            next_pos = self.pos + to_target * move_dist
            tile_world_pos = tile_to_pos(self.tile_pos)
            to_tile = (tile_world_pos - self.pos).normalize()
            next_to_tile = (tile_world_pos - next_pos).normalize()
            # check blocked
            if to_tile.dot(next_to_tile) <= 0:
                next_tile_pos = get_next_tile_pos(self.tile_pos, to_target) 
                if level_manager.is_blocked(next_tile_pos, self.actor):
                    # blocked, stop
                    target_pos = Vector(tile_world_pos)
                    dist = target_pos.distance(self.pos)
                    next_pos = Vector(target_pos)
                    self.target_positions.clear()
            # move    
            if dist <= move_dist:
                self.pos = target_pos
                if self.target_positions:
                    self.target_positions.pop()
            else:
                self.pos = next_pos
            self.front = to_target
            self.tile_pos = pos_to_tile(self.pos)
            return True
        return False