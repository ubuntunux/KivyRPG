import os
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.vector import Vector
from utility.kivy_helper import *
from .. import main

class TransformComponent():
    def __init__(self, pos):
        self.pos = Vector(pos)
        self.walk_speed = 1000.0
        self.target_pos = Vector(pos)
        self.is_complete = True
        
    def get_pos(self):
        return self.pos
        
    def move_to(self, pos):
        if pos != self.pos:
            self.is_complete = False
            self.target_pos = Vector(pos)
    
    def update_transform(self, dt):
        if False == self.is_complete:
            to_target = (self.target_pos - self.pos).normalize()
            move_dist = self.walk_speed * dt
            dist = self.target_pos.distance(self.pos)
            
            if dist <= move_dist:
                self.pos = self.target_pos
                self.is_complete = True
            else:
                self.pos = self.pos + to_target * move_dist
            return True
        return False 

class ActionData():
    def __init__(self, character_name, action_name, texture):
        self.action_data_path = os.path.join(character_name, action_name)
        self.name = action_name
        self.texture = texture


class CharacterData():
    def __init__(self, name, src_image, character_data_info):
        self.name = name
        self.action_data = {}
        action_data_infos = character_data_info.get("actions")
        for (action_name, action_data_info) in action_data_infos.items():
            texture = src_image.texture.get_region(*action_data_info["region"])
            self.action_data[action_name] = ActionData(name, action_name, texture)
    
    def get_action_data(self, action_name):
        return self.action_data.get(action_name)
        

class Character(Scatter):
    def __init__(self, character_data, pos, size, is_player):
        super().__init__(center=pos, size=size)
        self.image = Image(size=size, keep_ratio=False, allow_stretch=True)
        action_data = character_data.get_action_data("idle")
        if action_data:
            self.image.texture = action_data.texture  
        self.add_widget(self.image)
        
        self.transform_component = TransformComponent(pos)
        self.center = self.transform_component.get_pos()
        self.is_player = is_player

    def move_to(self, target_pos: Vector):
        self.transform_component.move_to(target_pos)
         
    def update(self, dt, force=False):
        updated = self.transform_component.update_transform(dt)
        if updated:
            self.center = self.transform_component.get_pos()