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
        
    def path_find(self, level_manager, tile_pos, target_tile_pos, target_dir, checked_list, paths, depth=0):
        #Logger.info((depth, "tile:", tile_pos, "target: ", target_tile_pos, "dir: ", target_dir))
        if 100 < depth:
            return False
        is_horizontal = abs(target_dir.y) < abs(target_dir.x)
        sign_x = sign(target_dir.x)
        sign_y = sign(target_dir.y)
        if sign_x == 0:
            sign_x = 1
        if sign_y == 0:
            sign_y = 1
        a = get_next_tile_pos(tile_pos, Vector(sign_x, 0) if is_horizontal else Vector(0, sign_y))
        b = get_next_tile_pos(tile_pos, Vector(0, sign_y) if is_horizontal else Vector(sign_x, 0))
        c = get_next_tile_pos(tile_pos, Vector(-sign_x,0) if is_horizontal else Vector(0, -sign_y))
        d = get_next_tile_pos(tile_pos, Vector(0, -sign_y) if is_horizontal else Vector(-sign_x, 0))
        points = [a,b,c,d]
        #Logger.info((depth, "points: ", points))
        for p in points:
            if p == target_tile_pos:
                paths.append(p)
                #Logger.info((depth, "arrive", p))
                return True
            is_in_checked_list = p in checked_list
            checked_list.append(p)
            if is_in_checked_list:
                #Logger.info((depth, "checked", p))
                continue
            elif level_manager.is_blocked(p, self.actor):
                #Logger.info((depth, "blocked", p))
                continue
            #Logger.info((">> next_tile_pos: ", p))
            next_target_dir = (target_tile_pos - p)
            find = self.path_find(level_manager, p, target_tile_pos, next_target_dir, checked_list, paths, depth+1)
            if find:
                paths.append(p)
                #Logger.info((depth, "find", p))
                return True
        #Logger.info((depth, "not found"))
        return False
            
    def move_to(self, level_manager, target_tile_pos):
        target_pos = tile_to_pos(target_tile_pos)
        if self.grid_based_movement:
            tile_world_pos = tile_to_pos(self.tile_pos)
            to_tile = tile_world_pos - self.pos
            is_vertical_line = abs(to_tile.x) < abs(to_tile.y)
            is_origin = (tile_world_pos == self.pos)
            to_target = target_pos - tile_world_pos
            checked_list = [Vector(self.tile_pos)]
            paths = []
            result = False
            if is_origin:
                result = self.path_find(level_manager, self.tile_pos, target_tile_pos, to_target, checked_list, paths) 
            else:
                next_tile_pos = Vector(self.tile_pos)
                component = 1 if is_vertical_line else 0
                if self.tile_pos[component] != target_tile_pos[component]:
                    next_tile_pos[component] += sign(to_target[component])
                    if level_manager.is_blocked(next_tile_pos, self.actor):
                        next_tile_pos = Vector(self.tile_pos)
                result = self.path_find(level_manager, next_tile_pos, target_tile_pos, to_target, checked_list, paths)
                paths.append(next_tile_pos)     
            self.target_positions = []
            if result:
                for p in paths:
                    self.target_positions.append(tile_to_pos(p))
            #Logger.info(("Result: ", self.target_positions))
            
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