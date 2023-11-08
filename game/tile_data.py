import os

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
 