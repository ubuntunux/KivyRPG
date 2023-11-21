import os
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from .. import main

class CharacterData():
    def __init__(self, character_set_name, character_name, texture):
        self.character_path = os.path.join(character_set_name, character_name)
        self.name = character_name
        self.texture = texture


class Character(Button):
    def __init__(self, character_data, pos, size):
        super().__init__(pos=pos, size=size)
        self.image = Image(texture=character_data.texture, pos=pos, size=size, keep_ratio=False, allow_stretch=True)
        self.add_widget(self.image)
        self.bind(on_press=self.on_pressed)
    
    def get_pixels(self):
        return list(self.image.texture.pixels)
    
    def on_pressed(self, inst):
        main.KivyRPGApp.instance().debug_print(str(inst))
        
    def update(self, dt):
        pass
 