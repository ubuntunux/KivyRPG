from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.vector import Vector
from utility.kivy_helper import *

class WeaponData():
    def __init__(self, resource_manager, name, weapon_data_info):
        self.name = name
        image = resource_manager.get_image(weapon_data_info.get("source", ""))
        region = weapon_data_info.get("region", (0,0,1,1))
        self.texture = None
        if image:
            self.texture = get_texture_atlas(image.texture, region)
        self.damage = weapon_data_info.get("damage", 10)
        self.size = weapon_data_info.get("size", (100,100))
        self.pos = weapon_data_info.get("pos", (50,0))


class Weapon(Scatter):
    def __init__(self, weapon_data):
        super().__init__(pos=weapon_data.pos, size=weapon_data.size)
        self.weapon_data = weapon_data
        self.image = Image(size=weapon_data.size, keep_ratio=False, allow_stretch=True)
        self.image.texture = weapon_data.texture
        self.add_widget(self.image)
        
        self.origin = Vector(self.pos)
        self.attack_anim_time = 0.0
    
    def on_touch_down(inst, touch):
        # do nothing
        return False
        
    def get_damage(self):
        return self.weapon_data.damage
    
    def set_attack(self):
        self.attack_anim_time = 0.1
    
    def update_weapon(self, dt):
        if 0 < self.attack_anim_time:
            self.attack_anim_time -= dt
            self.pos = add(self.origin, (100,0))
            if self.attack_anim_time <= 0:
                self.pos = Vector(self.origin)
            