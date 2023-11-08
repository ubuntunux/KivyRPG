from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from utility.singleton import SingletonInstance
from .game_resource import GameResourceManager


class Tile(Scatter):
    def __init__(self, tile_name, pos, size):
        super().__init__(pos=pos, size=size)
        tile_data = GameResourceManager.instance().get_tile_data(tile_name)
        image = Image(texture=tile_data.texture, size=size, keep_ratio=False, allow_stretch=True)
        self.add_widget(image)
    
    def update(self, dt):
        pass

class TileManager(Widget, SingletonInstance):
  def __init__(self, **kargs):
    Widget.__init__(self, **kargs)
  
  def reset_tiles(self):
    self.clear_widgets()
    
  def create_tile(self, tile_name, pos, size):
      tile = Tile(tile_name, pos, size)
      self.add_widget(tile)
      
  def update(self, dt):
      for child in self.children:
          child.update(dt)