from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from utility.singleton import SingletonInstance


class Tile(Scatter):
    def __init__(self, source, pos, size, texture_region):
        super().__init__(pos=pos, size=size)
        image = Image(source=source, size=size, keep_ratio=False, allow_stretch=True)
        image.texture = image.texture.get_region(*texture_region)
        self.add_widget(image)
    
    def update(self, dt):
        pass

class TileManager(Widget, SingletonInstance):
  def __init__(self, **kargs):
    Widget.__init__(self, **kargs)
  
  def reset_tiles(self):
    self.clear_widgets()
    
  def create_tile(self, source, pos, size, texture_region):
      tile = Tile(source, pos, size, texture_region)
      self.add_widget(tile)
      
  def update(self, dt):
      for child in self.children:
          child.update(dt)