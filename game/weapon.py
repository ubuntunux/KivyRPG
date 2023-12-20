from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from utility.kivy_helper import *

class WeaponData():
    def __init__(self, resource_manager, name, weapon_data_info):
        self.name = name
        image = resource_manager.get_image(weapon_data_info.get("source", ""))
        region = weapon_data_info.get("region", (0,0,1,1))
        self.texture = get_texture_atlas(texture, region)
        self.damage = weapon_data_info.get("damage", 10)
        self.size = weapon_data_info.get("size", (100,100))


class Weapon(Scatter):
    def __init__(self, pos, weapon_data):
        super().__init__(pos=pos, size=weapon_data.size)
        self.image = Image(size=weapon_data.size, keep_ratio=False, allow_stretch=True)
        self.image.texture = weapon_data.texture
        self.add_widget(self.image)
    
    def on_touch_down(inst, touch):
        # do nothing
        return False