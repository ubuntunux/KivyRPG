import os
import sys
import traceback

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from app.app import BaseApp, MainApp
from utility.singleton import SingletonInstance
from .game.tile import TileManager
from .game.resource import ResourceManager

class KivyRPGApp(BaseApp, SingletonInstance):
    def __init__(self, app_name):
        super(KivyRPGApp, self).__init__(app_name)
        self.resource_manager = ResourceManager.instance()
        self.tile_manager = TileManager.instance()
        
    def initialize(self):
        self.resource_manager.initialize()
        self.build() 

    def on_stop(self):
        pass
    
    def build(self):
        self.debug_text = Label(text="debug")
        self.add_widget(self.debug_text)
        #self.map_scroll_view = ScrollView(size_hint=(1, 1))
        #self.map_layout = BoxLayout(orientation="vertical", size=(2000,2000), size_hint=(None, None))
        self.add_widget(self.tile_manager)
        for y in range(16):
            for x in range(16):
                size=64
                texture_size=32
                self.tile_manager.create_tile(
                    source="KivyRPG/data/images/tiles_00.png",
                    pos=(size*x,size*y),
                    size=(size, size),
                    texture_region=(texture_size*x, texture_size*y, texture_size, texture_size)
                )
        
    def update(self, dt):
        self.tile_manager.update(dt)
    
