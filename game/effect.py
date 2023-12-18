from kivy.logger import Logger
from kivy.vector import Vector
from utility.effect import EffectManager
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
        
    def create_effect(self, effect_name, attach_to=None):
        game_resource = GameResourceManager.instance()
        effect_data = game_resource.get_effect_data(effect_name)
        if effect_data:
            emitter = self.create_emitter(
                emitter_name=effect_name,
                attach_to=attach_to,
                pos=(50,50),
                size=(100,100),
                effect_data=effect_data
            )
            emitter.play()