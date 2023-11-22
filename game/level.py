from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from utility.singleton import SingletonInstance
from .game_resource import GameResourceManager
from .tile import Tile


class LevelManager(SingletonInstance):
    def __init__(self, app):
        self.tile_map = None
        self.scroll_view = None
        self.tiles = []
        self.app = app
    
    def build(self, parent_widget):
        self.tile_map = Widget(size_hint=(None, None))
        self.scroll_view = ScrollView(size_hint=(1,1))
        self.scroll_view.add_widget(self.tile_map)
        parent_widget.add_widget(self.scroll_view)
        
    def reset_tiles(self):
        self.tiles.clear()
        self.tile_map.clear_widgets()
    
    def create_tile(self, tile_set_name, tile_name, tile_pos):
        tile_data_set = GameResourceManager.instance().get_tile_data_set(tile_set_name)  
        if tile_data_set:
            tile_data = tile_data_set.get_tile_data(tile_name)
            if tile_data:
                return Tile(tile_data, tile_pos)
      
    def open_level(self, level_name):
        self.reset_tiles()
        texture_size = 32
        stride = 4
        row_data_length = texture_size * stride
        
        num_x = 16
        num_y = 16
        width = num_x * texture_size
        height = num_y * texture_size
        texture_data_size = width * height * stride   
        # create texture
        texture = Texture.create(size=(width, height), colorfmt='rgba')
        data = ([int(255) for x in range(texture_data_size)])
        # set layout
        tile_image_size = 128
        self.tile_map.width = num_x * tile_image_size
        self.tile_map.height = num_y * tile_image_size
        
        for y in range(num_y):
            tiles = []
            for x in range(num_x):
                # create tile
                tile = self.create_tile(
                    tile_set_name="tile_set_00",
                    tile_name="grass",
                    tile_pos=(x, y)
                )
                # blit texture
                pixels = tile.get_pixels()
                for py in range(texture_size):
                    pixel_offset = py * texture_size * stride
                    data_offset = ((y * texture_size + py) * num_x + x) * texture_size * stride
                    data[data_offset: data_offset + row_data_length] = pixels[pixel_offset: pixel_offset + row_data_length] 
                tiles.append(tile)
            self.tiles.append(tiles)
        data = bytes(data)
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        with self.tile_map.canvas:
            Rectangle(texture=texture, size=self.tile_map.size)
        
    def update(self, dt):
        pass