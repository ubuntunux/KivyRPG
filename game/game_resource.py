import os
from kivy.logger import Logger
from kivy.uix.image import Image
from utility.singleton import SingletonInstance
from utility.resource import ResourceManager
from .tile_data import TileData, TileDataSet

game_path = "KivyRPG"
images_path = os.path.join(game_path, "data/images")
maps_path = os.path.join(game_path, "data/maps")
tile_data_path = os.path.join(game_path, "data/tiles")
   

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
                return TileDataSet(name, src_image, tile_data)
                
                