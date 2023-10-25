from kivy.uix.button import Button
from kivy.uix.widget import Widget
from utility.singleton import SingletonInstance
from utility.sprite import Sprite

class Tile(Sprite):
    def __init__(self, **kargs):
        super().__init__(**kargs)


class TileManager(Widget, SingletonInstance):
  def __init__(self, **kargs):
    Widget.__init__(self, **kargs)
  
  def reset_tiles(self):
    self.clear_widgets()
    
  def create_tile(self, **kargs):
      tile = Tile(**kargs)
      self.add_widget(tile)
      
  def update(self, dt):
      pass