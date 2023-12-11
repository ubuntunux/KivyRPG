from enum import Enum
import os
from kivy.logger import Logger
from kivy.graphics.transformation import Matrix
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.vector import Vector
from utility.kivy_helper import *
from .behavior import *
from .transform_component import TransformComponent
from .constant import *
from .. import main

 
class ActionState(Enum):
    IDLE = 0
    ATTACK = 1


class ActionData():
    def __init__(self, character_name, action_name, texture):
        self.action_data_path = os.path.join(character_name, action_name)
        self.name = action_name
        self.texture = texture


class Action():
    def __init__(self, action_data):
        self.action_data = action_data
        self.action_state = ActionState.IDLE
        self.action_time = 0.0
    
    def get_action_state(self):
        return self.action_state
    
    def set_action_state(self, action_state):
        self.action_state = action_state
        self.action_time = 0.5
        
    def get_current_texture(self):
        action_data = self.action_data.get("idle")
        if action_data:
             return action_data.texture
        return None
        
    def update_action(self, dt):
        if ActionState.IDLE != self.action_state:
            if self.action_time < 0:
                self.set_action_state(ActionState.IDLE)
        
        if 0 < self.action_time:
            self.action_time -= dt


class CharacterData():
    def __init__(self, name, src_image, character_data_info):
        self.name = name
        self.action_data = {}
        action_data_infos = character_data_info.get("actions")
        for (action_name, action_data_info) in action_data_infos.items():
            texture = src_image.texture.get_region(*action_data_info["region"])
            self.action_data[action_name] = ActionData(name, action_name, texture)
        self.behavior_class = eval(character_data_info.get("behavior_class"))
        self.properties = character_data_info.get("properties", {})


class Character(Scatter):
    def __init__(self, character_data, tile_pos, size, is_player):
        super().__init__(size=size)
        
        self.action = Action(character_data.action_data)
        self.image = Image(size=size, keep_ratio=False, allow_stretch=True)
        self.image.texture = self.action.get_current_texture()
        self.add_widget(self.image)
        
        self.properties = character_data.properties  
        self.behavior = character_data.behavior_class(self)
        self.transform_component = TransformComponent(self, tile_pos, self.properties)
        self.center = self.transform_component.get_pos()
        self.updated_pos = True
        self.updated_tile_pos = True
        self.spawn_tile_pos = Vector(tile_pos)
        self.is_player = is_player
    
    def on_touch_down(inst, touch):
        # do nothing
        return False
        
    def flip_widget(self):
        self.apply_transform(
            Matrix().scale(-1.0, 1.0, 1.0),
            post_multiply=True,
            anchor=self.to_local(*self.center)
        )
    
    def move_to(self, level_manager, tile_pos):
        self.transform_component.trace_actor(level_manager, None)
        self.transform_component.move_to(level_manager, tile_pos)
    
    def trace_actor(self, level_manager, actor):
        self.transform_component.trace_actor(level_manager, actor)
         
    def get_spawn_tile_pos(self):
        return self.spawn_tile_pos
    
    def set_spawn_tile_pos(self, spawn_tile_pos):
        self.spawn_tile_pos = Vector(spawn_tile_pos)
        
    def get_attack_point(self):
        if ActionState.ATTACK == self.action.get_action_state():
            return get_next_tile_pos(self.get_tile_pos(), self.get_front())
        return None
        
    def set_attack(self):
        self.action.set_action_state(ActionState.ATTACK)
    
    def get_front(self):
        return self.transform_component.get_front()

    def get_direction_x(self):
        return sign(self.transform[0])
    
    def get_pos(self):
        return self.transform_component.get_pos()
    
    def get_tile_pos(self):
        return self.transform_component.get_tile_pos()
    
    def get_prev_pos(self):
        return self.transform_component.get_prev_pos()
    
    def get_prev_tile_pos(self):
        return self.transform_component.get_prev_tile_pos()
    
    def get_coverage_tile_pos(self):
        return self.transform_component.get_coverage_tile_pos()
             
    def get_updated_pos(self):
        return self.updated_pos
        
    def get_updated_tile_pos(self):
        return self.updated_tile_pos
    
    def update(self, actor_manager, level_manager, dt):
        self.behavior.update_behavior(actor_manager, level_manager, dt)
        self.action.update_action(dt)
        self.updated_pos = self.transform_component.update_transform(level_manager, dt)
        self.updated_tile_pos = self.get_prev_tile_pos() != self.get_tile_pos()
        if self.updated_pos:
            self.center = self.transform_component.get_pos()
            prev_direction_x = self.get_direction_x()
            curr_front_x = sign(self.transform_component.front.x)
            if 0 != curr_front_x and prev_direction_x != curr_front_x:
                self.flip_widget()
            