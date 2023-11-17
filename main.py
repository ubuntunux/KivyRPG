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
from utility.kivy_widgets import DebugLabel
from utility.singleton import SingletonInstance
from .game.level import LevelManager
from .game.game_resource import GameResourceManager


class KivyRPGApp(BaseApp, SingletonInstance):
    def __init__(self, app_name):
        super(KivyRPGApp, self).__init__(app_name)
        self.resource_manager = GameResourceManager.instance()
        self.level_manager = LevelManager.instance()
        self.debug_label = None
        
    def initialize(self):
        self.resource_manager.initialize()
        self.build() 

    def on_stop(self):
        pass
        
    def build(self):
        self.level_manager.build(self)
        self.level_manager.open_level("default")
        
        # print debug
        self.debug_label = DebugLabel(
            pos=(0, self.height),
            text="debug", 
            halign='left',
            font_size="12sp",
            size_hint=(None, None),
            width=self.width
        )
        self.add_widget(self.debug_label)
        
    def debug_print(self, text):
        self.debug_label.debug_print(text)
        
    def update(self, dt):
        self.debug_label.update(dt)
        self.debug_label.pos = (0, self.height - self.debug_label.height)
        
        self.level_manager.update(dt)
        