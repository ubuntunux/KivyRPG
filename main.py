import os
import sys
import traceback

from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from app.app import BaseApp, MainApp
from utility.kivy_widgets import KivyLabel
from utility.singleton import SingletonInstance
from .game.tile import TileManager
from .game.game_resource import GameResourceManager


class KivyRPGApp(BaseApp, SingletonInstance):
    def __init__(self, app_name):
        super(KivyRPGApp, self).__init__(app_name)
        self.resource_manager = GameResourceManager.instance()
        self.tile_manager = TileManager.instance()
        
    def initialize(self):
        self.resource_manager.initialize()
        self.build() 

    def on_stop(self):
        pass
    
    def build(self):
        self.add_widget(self.tile_manager)
        for y in range(16):
            for x in range(16):
                size=64
                texture_size=32
                self.tile_manager.create_tile(
                    source="KivyRPG/data/images/tiles_00.png",
                    pos=(size*x,size*y),
                    size=(size, size),
                    texture_region=(
                        texture_size*x, 
                        texture_size*y,
                        texture_size,
                        texture_size
                    )
                )
        # print debug
        self.debug_text = KivyLabel(
            text="debug", 
            halign='left',
            font_size="12sp",
            size_hint=(None, None),
            width=self.width
        )
        self.add_widget(self.debug_text)
        
    def update_debug_print(self):
        fps = Clock.get_fps()
        time = 1000.0 / fps if 0 < fps else 0
        self.debug_text.text = f"fps: {format(fps, '0.2f')}\ntime(ms): {format(time, '0.2f')}"
        self.debug_text.height = self.debug_text.minimum_height
        self.debug_text.pos = (0, self.height - self.debug_text.height)
       
    def update(self, dt):
        self.update_debug_print()
        self.tile_manager.update(dt)
        