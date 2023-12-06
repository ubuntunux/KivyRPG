from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from utility.kivy_helper import *
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
        self.actors = []
        self.actor_map = {}
        self.app = app
        self.actor_manager = None
        self.num_x = 16
        self.num_y = 16
        
    def initialize(self, parent_widget, actor_manager):
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
        self.actor_manager.callback_touch(inst, touch)
        return True
    
    def index_to_pos(self, index):
        y = int(index / self.num_x)
        x = index - y
        return (x, y)
        
    def pos_to_index(self, pos):
        return int(pos[1] * self.num_x + pos[0])
    
    def is_in_level(self, tile_pos):
        return 0 <= tile_pos.x and tile_pos.x <= (self.num_x - 1) and 0 <= tile_pos.y and tile_pos.y <= (self.num_y - 1)
    
    def is_blocked(self, pos, filter_actor=None):
        actor = self.get_actor(pos)
        return actor is not filter_actor and actor is not None
    
    def get_actor_area(self, actor):
        return self.actor_map.get(actor, [])
        
    def get_actor(self, pos):
        index = self.pos_to_index(pos)
        if index < len(self.actors):
            return self.actors[index]
        return None
        
    def set_actor(self, actor):
        # remove
        old_area = self.get_actor_area(actor)
        for old_pos in old_area:
            index = self.pos_to_index(old_pos)
            if index < len(self.actors):
                self.actors[index] = None
        if self.actor_map.get(actor) is not None:
            self.actor_map.pop(actor)
        # set
        main_tile_pos = actor.get_tile_pos()
        tile_to_actor = actor.get_pos() - tile_to_pos(main_tile_pos)
        coverage_tile = get_next_tile_pos(main_tile_pos, tile_to_actor)
        area = [main_tile_pos]
        if main_tile_pos != coverage_tile:
            area.append(coverage_tile)
        for tile_pos in area:
            index = self.pos_to_index(tile_pos)
            if index < len(self.actors):
                self.actors[index] = actor
        self.actor_map[actor] = area    
    
    def reset_tiles(self):
        self.actor_map.clear()
        self.actors.clear()
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
        self.num_x = 16
        self.num_y = 16
        num_tiles = self.num_x * self.num_y
        self.actors = [None for i in range(num_tiles)]
        
        texture_size = 32
        stride = 4
        row_data_length = texture_size * stride
        width = self.num_x * texture_size
        height = self.num_y * texture_size
        texture_data_size = width * height * stride   
        # create texture
        texture = Texture.create(size=(width, height), colorfmt='rgba')
        data = ([int(255) for x in range(texture_data_size)])
        # set layout
        self.tile_map.width = self.num_x * TILE_WIDTH
        self.tile_map.height = self.num_y * TILE_HEIGHT
        self.top_layer.size = self.tile_map.size
        for y in range(self.num_y):
            tiles = []
            for x in range(self.num_x):
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
                    data_offset = ((y * texture_size + py) * self.num_x + x) * texture_size * stride
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