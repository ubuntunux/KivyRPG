import os
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from .. import main

class ActionData():
    def __init__(self, character_name, action_name, texture):
        self.action_data_path = os.path.join(character_name, action_name)
        self.name = action_name
        self.texture = texture


class CharacterData():
    def __init__(self, resource_manager, name, src_image, character_data_info):
        self.name = name
        self.action_data = {}
        src_image = resource_manager.get_image(data["source"])
        action_data_infos = character_data_info.get("actions")
        for (action_name, action_data_info) in action_data_infos.items():
            texture = src_image.texture.get_region(*action_data_info["region"])
            self.action_data[action_name] = CharacterData(name, action_name, texture)
    
    def get_action_data(self, action_name):
        return self.action_data.get(action_name)
        

class Character(Button):
    def __init__(self, character_data, pos, size):
        super().__init__(pos=pos, size=size)
        action_data = character_data.get_action_data("idle")
        self.image = Image(texture=action_data.texture, pos=pos, size=size, keep_ratio=False, allow_stretch=True)
        self.add_widget(self.image)
        self.bind(on_press=self.on_pressed)
    
    def on_pressed(self, inst):
        main.KivyRPGApp.instance().debug_print(str(inst))
        
    def update(self, dt):
        pass
 