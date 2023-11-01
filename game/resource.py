import os
from utility.singleton import SingletonInstance

game_path = "KivyRPG"
images_path = os.path.join(game_path, "data/images")
maps_path = os.path.join(game_path, "data/maps")
tiles_path = os.path.join(game_path, "data/tiles")

class Resource:
    def __init__(self, name, filepath, loader):
        self.name = name
        self.is_loaded = False
        self.loader = loader
        self.filepath = filepath
        self.source = None
        

class ResourceManager(SingletonInstance):
    def __init__(self):
        super(ResourceManager, self).__init__()
        self.images = {}
        self.tiles = {}
        
    def initialize(self):
        self.register_resources(images_path, [".png", ".jpg"], self.images, self.image_loader)
        self.register_resources(tiles_path, [".data"], self.tiles, self.tile_loader)
    
    def register_resources(self, resource_path, resource_exts, resource_map, resource_loader):
        for dirname, dirnames, filenames in os.walk(resource_path):
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in resource_exts:
                    filepath = os.path.join(dirname, filename)
                    resource_name = os.path.relpath(filepath, resource_path)
                    resource_name = os.path.splitext(resource_name)[0]
                    from kivy.logger import Logger
                    Logger.info(resource_name)
                    resource_map[resource_name] = Resource(
                        resource_name,
                        filename,
                        resource_loader
                    )
                    
    def image_loader(self, filepath):
        pass
        
    def tile_loader(self, filepath):
        pass