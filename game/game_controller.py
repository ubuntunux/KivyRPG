from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from utility.kivy_helper import *
from utility.singleton import SingletonInstance
from .level import LevelManager
from .actor import ActorManager
from .game_resource import GameResourceManager
from .constant import *


class DirectionController():
    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.pressed_direction = ""
        
    def initialize(self, controller_layer):
        self.pressed_direction = False
        
        def create_button(text, pos):
            btn = Button(text=text, pos=pos, size_hint=(None, None), size=(150, 150), opacity=0.5)
            btn.bind(on_press=self.on_presse_direction, on_release=self.on_release_direction)
            controller_layer.add_widget(btn)
        create_button("left", (10,160))
        create_button("up", (160,310))
        create_button("down", (160,10))
        create_button("right", (310,160))
    
    def on_presse_direction(self, inst):
        self.pressed_direction = inst.text
    
    def on_release_direction(self, inst):
        self.pressed_direction = ""
    
    def update(self, dt):
        if self.pressed_direction:
            self.game_controller.pressed_direction(self.pressed_direction)
        
        
class GameController(SingletonInstance):
    def __init__(self, app):
        self.app = app
        self.actor_manager = None
        self.level_manager = None
        self.direction_controller = DirectionController(self)
        
    def initialize(self, parent_widget, level_manager, actor_manager):
        self.level_manager = level_manager
        self.actor_manager = actor_manager
        self.controller_layer = FloatLayout(size_hint=(1,1))
        
        self.direction_controller.initialize(self.controller_layer)
        
        # attack button
        btn = Button(text="Attack", pos_hint={"right":1}, size_hint=(None, None), size=(300, 300), opacity=0.5)
        btn.bind(on_press=actor_manager.callback_attack)
        self.controller_layer.add_widget(btn)
        
        parent_widget.add_widget(self.controller_layer)
    
    def pressed_direction(self, direction):
        self.actor_manager.callback_move(direction)
    
    def update(self, dt):
        self.direction_controller.update(dt)
        
        
    