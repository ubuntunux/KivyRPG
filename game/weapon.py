import copy
from kivy.graphics.transformation import Matrix
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.vector import Vector
from utility.kivy_helper import *
from .effect import GameEffectManager


class Weapon(Scatter):
    def __init__(self, actor, weapon_data):
        super().__init__(pos=weapon_data.pos, size=weapon_data.size)
        self.weapon_data = weapon_data
        self.image = Image(size=weapon_data.size, keep_ratio=False, allow_stretch=True)
        self.image.texture = weapon_data.texture
        self.add_widget(self.image)
        
        self.origin = Vector(self.pos)
        self.attack_anim_time = 0.0
        self.attack_dir = Vector(1,0)
        self.actor = actor
    
    def on_touch_down(inst, touch):
        # do nothing
        return False
        
    def get_damage(self):
        return self.weapon_data.damage
    
    def set_attack(self, attack_dir):
        self.attack_anim_time = 0.1
        self.attack_dir = Vector(attack_dir)
        self.update_weapon_transform(attack_dir, 50.0)
        if self.weapon_data.attack_effect:
            GameEffectManager.instance().create_effect(
                self.weapon_data.attack_effect,
                attach_to=self
            )
            
    def update_weapon_transform(self, attack_dir, distance):
        if abs(attack_dir.x) < abs(attack_dir.y):
            sign_y = sign(attack_dir.y)
            self.pos = Vector(self.origin.y, (self.origin.x + distance) * sign_y)
            self.rotation = 90 * sign_y
        else:
            self.pos = Vector(self.origin.x + distance, self.origin.y)
            self.rotation = 0
        
    def update_weapon(self, dt):
        if 0 < self.attack_anim_time:
            self.attack_anim_time -= dt
            if self.attack_anim_time <= 0:
                self.update_weapon_transform(self.attack_dir, 0.0)
            
   