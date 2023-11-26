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
from .constant import *


class LevelManager(SingletonInstance):
    def __init__(self, app):
        self.tile_map = None
        self.character_layer = None
        self.top_layer = None
        self.scroll_view = None
        self.tiles = []
        self.app = app
        self.actor_manager = None
        
    def initialize(self, actor_manager, parent_widget):
        self.actor_manager = actor_manager
        self.tile_map = Widget(size_hint=(None, None))
        self.tile_map.bind(on_touch_down=self.on_touch_down)
        self.character_layer = Widget(size_hint=(None, None))
        self.top_layer = Widget(size_hint=(None, None))
        self.scroll_view = ScrollView(size_hint=(1,1))
        # link
        self.top_layer.add_widget(self.tile_map)
        self.top_layer.add_widget(self.character_layer)
        self.scroll_view.add_widget(self.top_layer)
        parent_widget.add_widget(self.scroll_view)
        
    def on_touch_down(self, inst, touch):
        #self.app.debug_print(str(touch.pos))
        self.actor_manager.get_player().move_to(touch.pos)
    
    def reset_tiles(self):
        self.tiles.clear()
        self.tile_map.clear_widgets()
        self.character_layer.clear_widgets()
    
    def create_tile(self, tile_set_name, tile_name, tile_pos):
        tile_data_set = GameResourceManager.instance().get_tile_data_set(tile_set_name)  
        if tile_data_set:
            tile_data = tile_data_set.get_tile_data(tile_name)
            if tile_data:
                return Tile(tile_data, tile_pos)
      
    def generate_tile_map(self, level_name):
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
        self.tile_map.width = num_x * TILE_WIDTH
        self.tile_map.height = num_y * TILE_HEIGHT
        self.top_layer.size = self.tile_map.size
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
        
    def open_level(self, level_name):
        self.generate_tile_map(level_name)
        self.actor_manager.create_actors(self.top_layer)
    
    def update(self, dt):
        pass