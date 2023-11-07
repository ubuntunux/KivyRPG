import os
from kivy.logger import Logger
from kivy.uix.image import Image
from utility.singleton import SingletonInstance
from utility.resource import ResourceManager

game_path = "KivyRPG"
images_path = os.path.join(game_path, "data/images")
maps_path = os.path.join(game_path, "data/maps")
tiles_path = os.path.join(game_path, "data/tiles")


class GameResourceManager(ResourceManager):
    def __init__(self):
        super(GameResourceManager, self).__init__()
        self.images = {}
        self.tiles ={}
    
    def initialize(self):
        self.register_resources(images_path, [".png", ".jpg"], self.images, self.image_loader)
        self.register_resources(tiles_path, [".data"], self.tiles, self.tile_loader)
    
    def get_image(self, resource_name):
        return self.get_resource(self.images, resource_name)
    
    def get_tile(self, resource_name):
        return self.get_resource(self.tiles, resource_name)
        
    def image_loader(self, filepath):
        return Image(source=filepath)
    
    def tile_loader(self, filepath):
        pass