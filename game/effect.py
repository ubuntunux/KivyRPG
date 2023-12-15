from kivy.logger import Logger
from kivy.vector import Vector
from utility.particle import EffectManager
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
        particle_data = game_resource.get_particle_data("explosion")
        emitter = self.create_emitter(
            emitter_name='explosion',
            attach_to=None,
            pos=(50,50),
            size=(100,100),
            particle_data=particle_data.get_data(),
            particle_count=20
        )
        emitter.play()