from kivy.logger import Logger
from kivy.vector import Vector
from utility.particle import EffectManager, Particle
from utility.singleton import SingletonInstance
from utility.kivy_helper import *
from utility.range_variable import RangeVar
from .game_resource import GameResourceManager
from .constant import *


class FxManager(EffectManager):
    def __init__(self, app):
        super(FxManager, self).__init__()
        self.app = app
        self.level_manager = None
        
    def initialize(self, level_manager, effect_layout):
        self.level_manager = level_manager
        super(FxManager, self).initialize(effect_layout)
        
    def create_effects(self, player):
        game_resource = GameResourceManager.instance()
        particle_info = dict(
            loop=-1,
            fade=1,
            color=(1,1,1,1),
            collision=True,
            texture=game_resource.get_image("explosion").texture,
            delay=RangeVar(0.0,1.0), 
            angular_velocity=RangeVar(360.0), 
            rotate=RangeVar(0.0, 360), 
            offset=RangeVar((-20,20), (-20,20)),
            life_time=RangeVar(5.5,5.5), 
            sequence=[4,4],
            velocity=RangeVar([-2000.0, 100], [2000.0, 200]),
            gravity=RangeVar(900.0)
        )
        self.create_emitter('explosion', particle_info, 20, pos=(50,50), size=(100,100))
        effect = self.get_emitter('explosion')
        effect.play_particle(None, True)
        