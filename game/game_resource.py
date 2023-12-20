import os
from kivy.logger import Logger
from utility.singleton import SingletonInstance
from utility.resource import ResourceManager
from .character_data import CharacterData
from .tile import TileData, TileDataSet
from .weapon import WeaponData


game_path = "KivyRPG"
effects_path = os.path.join(game_path, "data/effects")
images_path = os.path.join(game_path, "data/images")
maps_path = os.path.join(game_path, "data/maps")
tile_data_path = os.path.join(game_path, "data/tiles")
character_data_path = os.path.join(game_path, "data/characters")
weapon_data_path = os.path.join(game_path, "data/weapons")
 

class GameResourceManager(ResourceManager):
    def __init__(self):
        super(GameResourceManager, self).__init__()
        self.tile_data_set = {}
        self.character_data = {}
        self.weapon_data = {}
    
    def initialize(self):
        self.register_resources(images_path, [".png", ".jpg"], self.images, self.image_loader)
        self.register_resources(effects_path, [".data"], self.effect_data, self.effect_data_loader)
        self.register_resources(tile_data_path, [".data"], self.tile_data_set, self.tile_data_set_loader)
        self.register_resources(character_data_path, [".data"], self.character_data, self.character_data_loader)
        self.register_resources(weapon_data_path, [".data"], self.weapon_data, self.weapon_data_loader)
    
    # tile
    def get_tile_data_set(self, resource_name):
        return self.get_resource(self.tile_data_set, resource_name)
        
    def tile_data_set_loader(self, name, filepath):
        if os.path.exists(filepath):
            with open(filepath) as f:
                tile_data_set_info = eval(f.read())
                return TileDataSet(self, name, tile_data_set_info)
    
    # character
    def get_character_data(self, resource_name):
        return self.get_resource(self.character_data, resource_name)
        
    def character_data_loader(self, name, filepath):
        if os.path.exists(filepath):
            with open(filepath) as f:
                character_data_info = eval(f.read())
                return CharacterData(self, name, character_data_info)
                
    # weapon
    def get_weapon_data(self, resource_name):
        return self.get_resource(self.weapon_data, resource_name)
        
    def weapon_data_loader(self, name, filepath):
        if os.path.exists(filepath):
            with open(filepath) as f:
                weapon_data_info = eval(f.read())
                return WeaponData(self, name, weapon_data_info)
                
                