from kivy.uix.widget import Widget
from utility.singleton import SingletonInstance
from .game_resource import GameResourceManager
from .tile import Tile


class LevelManager(Widget, SingletonInstance):
    def __init__(self, **kargs):
      Widget.__init__(self, **kargs)
  
    def reset_tiles(self):
      self.clear_widgets()
    
    def create_tile(self, tile_name, pos, size):
        tile_data = GameResourceManager.instance().get_tile_data(tile_name)  
        tile = Tile(tile_data, pos, size)
        self.add_widget(tile)
      
    def open_level(self, level_name):
        self.reset_tiles()
        for y in range(16):
            for x in range(16):
                size=64
                texture_size=32
                self.create_tile(
                    tile_name="tile_set_00/grass",
                    pos=(size*x,size*y),
                    size=(size, size)
                )

    def update(self, dt):
        pass