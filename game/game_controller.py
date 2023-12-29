from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
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
        self.button_active_opacity = 0.5
        self.button_deactive_opacity = 0.2
        self.button_bounds = (10,10,210,210)
        self.button_neutral_pos = (
            (self.button_bounds[0] + self.button_bounds[2]) * 0.5,
            (self.button_bounds[1] + self.button_bounds[3]) * 0.5
        )
        self.dead_zone_size = 10
        self.button = None
        self.button_color = Color(1,1,1,1)
        self.touch_id = None
        
    def initialize(self, controller_layer):
        resource_manager = GameResourceManager.instance()
        self.button = Scatter(
            do_rotation=False,
            do_scale=False,
            do_translation=False,
            pos=self.button_neutral_pos,
            size_hint=(None, None),
            size=(200, 200)
        )
        self.button.bind(
            on_touch_down=self.on_touch_down,
            on_touch_move=self.on_touch_move,
            on_touch_up=self.on_touch_up
        )
        with self.button.canvas:
            self.button_color = Color(1,1,1, self.button_deactive_opacity)
            Rectangle(size=self.button.size)
        
        add_image = False
        if add_image:
            point = resource_manager.get_image("point")
            img_pos = mul(self.button.size, -0.5)
            img_size = mul(self.button.size, 2.0)
            img = Image(texture=point.texture, pos=img_pos, size=img_size, keep_ratio=False, allow_stretch=True)
            self.button.add_widget(img)
      
        controller_layer.add_widget(self.button)
        
    def on_touch_down(self, inst, touch):
        if self.touch_id is None and inst.collide_point(*touch.pos):
            self.set_button_center(touch.pos)
            self.button_color.a = self.button_active_opacity
            self.touch_id = touch.id
            return True
        return False
    
    def on_touch_move(self, inst, touch):
        if self.touch_id == touch.id:
            self.set_button_center(touch.pos)
            return True
        return False
        
    def on_touch_up(self, inst, touch):
        if self.touch_id == touch.id:
            self.set_button_pos(self.button_neutral_pos)
            self.button_color.a = self.button_deactive_opacity
            self.touch_id = None
            return True
        return False
    
    def set_button_center(self, pos):
        self.set_button_pos(sub(pos, mul(self.button.size, 0.5)))
    
    def set_button_pos(self, pos):
        bounds = self.button_bounds
        self.button.pos = (
            max(bounds[0], min(bounds[2], pos[0])),
            max(bounds[1], min(bounds[3], pos[1]))
        )
        
    def update(self, dt):
        if self.touch_id is not None:
            diff = sub(self.button.pos, self.button_neutral_pos)
            mag_x = max(0, abs(diff[0]) - self.dead_zone_size)
            mag_y = max(0, abs(diff[1]) - self.dead_zone_size)
            direction = None
            if mag_x < mag_y:
                if 0 < sign(diff[1]):
                    direction = "up"
                else:
                    direction = "down"
            elif mag_y < mag_x:
                if 0 < sign(diff[0]):
                    direction = "right"
                else:
                    direction = "left"
            log_info((diff, direction))
            if direction:
                self.game_controller.pressed_direction(direction)
        
        
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
        
        
    