import os
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from .. import main
class TileData():
    def __init__(self, tile_set_name, tile_name, texture):
        self.tile_path = os.path.join(tile_set_name, tile_name)
        self.name = tile_name
        self.texture = texture


class TileDataSet():
    def __init__(self, name, src_image, tile_data):
        self.name = name
        self.tile_data = {}
        for (tile_name, tile_data_info) in tile_data.items():
            texture = src_image.texture.get_region(*tile_data_info["region"])
            self.tile_data[tile_name] = TileData(name, tile_name, texture)
    
    def get_tile_data(self, tile_name):
        return self.tile_data.get(tile_name)
        

class Tile(Button):
    def __init__(self, tile_data, pos, size):
        super().__init__(pos=pos, size=size)
        self.image = Image(texture=tile_data.texture, pos=pos, size=size, keep_ratio=False, allow_stretch=True)
        self.add_widget(self.image)
        self.bind(on_press=self.on_pressed)
    
    def get_pixels(self):
        return list(self.image.texture.pixels)
    
    def on_pressed(self, inst):
        main.KivyRPGApp.instance().debug_print(str(inst))
        
    def update(self, dt):
        pass
 