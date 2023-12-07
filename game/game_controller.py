from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from utility.kivy_helper import *
from utility.singleton import SingletonInstance
from .level import LevelManager
from .actor import ActorManager
from .game_resource import GameResourceManager
from .constant import *


class GameController(SingletonInstance):
    def __init__(self, app):
        self.app = app
        self.actor_manager = None
        self.level_manager = None
        
    def initialize(self, parent_widget, level_manager, actor_manager):
        self.level_manager = level_manager
        self.actor_manager = actor_manager
        self.controller_layer = Widget(size_hint=(None, None))
        btn = Button(text="Button", pos=(Window.width-300,0), size=(300, 300), opacity=0.5)
        btn.bind(on_press=actor_manager.callback_attack)
        self.controller_layer.add_widget(btn)
        parent_widget.add_widget(self.controller_layer)
        
    