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
    def __init__(self, tile_data):
        src_image = GameResourceManager.instance().get_image(tile_data["source"])
        self.texture = src_image.texture.get_region(*tile_data["region"])


class GameResourceManager(ResourceManager):
    def __init__(self):
        super(GameResourceManager, self).__init__()
        self.images = {}
        self.tile_data ={}
    
    def initialize(self):
        self.register_resources(images_path, [".png", ".jpg"], self.images, self.image_loader)
        self.register_resources(tile_data_path, [".data"], self.tile_data, self.tile_data_loader)
    
    def get_image(self, resource_name):
        return self.get_resource(self.images, resource_name)
    
    def get_tile_data(self, resource_name):
        return self.get_resource(self.tile_data, resource_name)
        
    def image_loader(self, filepath):
        return Image(source=filepath)
    
    def tile_data_loader(self, filepath):
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = eval(f.read())
                return TileData(data)
                
                