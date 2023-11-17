from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from utility.singleton import SingletonInstance
from .game_resource import GameResourceManager
from .tile import Tile


class LevelManager(SingletonInstance):
    def __init__(self):
        self.layout = None
        self.scroll_view = None
        self.tiles = []
    
    def build(self, parent_widget):
        self.layout = Widget(size_hint=(None, None))
        self.scroll_view = ScrollView(size_hint=(1,1))
        self.scroll_view.add_widget(self.layout)
        parent_widget.add_widget(self.scroll_view)
        
    def reset_tiles(self):
        self.tiles.clear()
        self.layout.clear_widgets()
    
    def create_tile(self, tile_name, pos, size):
        tile_data = GameResourceManager.instance().get_tile_data(tile_name)  
        tile = Tile(tile_data, pos, size)
        self.layout.add_widget(tile)
        return tile
      
    def open_level(self, level_name):
        self.reset_tiles()
        num_x = 32
        num_y = 32
        tile_size = 128
        for y in range(num_y):
            tiles = []
            for x in range(num_x):
                tile = self.create_tile(
                    tile_name="tile_set_00/grass",
                    pos=(tile_size * x, tile_size * y),
                    size=(tile_size, tile_size)
                )
                tiles.append(tile)
            self.tiles.append(tiles)
        self.layout.width = tile_size * num_x
        self.layout.height = tile_size * num_y

    def update(self, dt):
        pass