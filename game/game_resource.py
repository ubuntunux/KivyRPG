import os
from kivy.logger import Logger
from kivy.uix.image import Image
from utility.singleton import SingletonInstance
from utility.resource import ResourceManager

game_path = "KivyRPG"
images_path = os.path.join(game_path, "data/images")
maps_path = os.path.join(game_path, "data/maps")
tile_data_path = os.path.join(game_path, "data/tiles")


class TileData():
    def __init__(self, tile_set_name, tile_name, texture):
        self.tile_path = os.path.join(tile_set_name, tile_name)
        self.name = tile_name
        self.texture = texture

class TileSet():
    def __init__(self, name, src_image, tile_data):
        self.name = name
        self.tile_data = {}
        for (tile_name, tile_data_info) in tile_data.items():
            texture = src_image.texture.get_region(*tile_data_info["region"])
            self.tile_data[tile_name] = TileData(name, tile_name, texture)
    
    def get_tile_data(self, tile_name):
        return self.tile_data.get(tile_name)
    

class GameResourceManager(ResourceManager):
    def __init__(self):
        super(GameResourceManager, self).__init__()
        self.images = {}
        self.tile_data_set ={}
    
    def initialize(self):
        self.register_resources(images_path, [".png", ".jpg"], self.images, self.image_loader)
        self.register_resources(tile_data_path, [".data"], self.tile_data_set, self.tile_data_loader)
    
    def get_image(self, resource_name):
        return self.get_resource(self.images, resource_name)
    
    def get_tile_data(self, resource_name):
        (tile_data_set_name, tile_data_name) = os.path.split(resource_name)
        tile_data_set = self.get_resource(self.tile_data_set, tile_data_set_name)
        if tile_data_set:
            return tile_data_set.get_tile_data(tile_data_name)
        
    def image_loader(self, name, filepath):
        return Image(source=filepath)
    
    def tile_data_loader(self, name, filepath):
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = eval(f.read())
                src_image = self.get_image(data["source"])
                tile_data = data["tile_data"]
                return TileSet(name, src_image, tile_data)
                
                