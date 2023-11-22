import os
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from utility.kivy_helper import *
from .. import main

class ActionData():
    def __init__(self, character_name, action_name, texture):
        self.action_data_path = os.path.join(character_name, action_name)
        self.name = action_name
        self.texture = texture


class CharacterData():
    def __init__(self, name, src_image, character_data_info):
        self.name = name
        self.action_data = {}
        Logger.info("name " + name)
        Logger.info("image " + str(src_image))
        Logger.info("data " + str(character_data_info))
        action_data_infos = character_data_info.get("actions")
        for (action_name, action_data_info) in action_data_infos.items():
            texture = src_image.texture.get_region(*action_data_info["region"])
            self.action_data[action_name] = ActionData(name, action_name, texture)
    
    def get_action_data(self, action_name):
        return self.action_data.get(action_name)
        

class Character(Scatter):
    def __init__(self, character_data, pos, size):
        super().__init__(pos=pos, size=size)
        flip_widget(self)
        action_data = character_data.get_action_data("idle")
        self.image = Image(texture=action_data.texture, pos=pos, size=size, keep_ratio=False, allow_stretch=True)
        self.add_widget(self.image)
        self.bind(on_touch_down=self.on_touch_down)
    
    def on_touch_down(self, *args):
        main.KivyRPGApp.instance().debug_print(str(self.image.texture_size))
        
    def update(self, dt):
        pass
 