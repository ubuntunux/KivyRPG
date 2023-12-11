from kivy.logger import Logger
from kivy.vector import Vector
from utility.singleton import SingletonInstance
from utility.kivy_helper import *
from .game_resource import GameResourceManager
from .constant import *


class EffectManager(SingletonInstance):
    def __init__(self, app):
        self.app = app
        self.level_manager = None
        self.effect_layout = None
        self.effects = []
        self.player = None
        
    def initialize(self, level_manager, effect_layout):
        self.level_manager = level_manager
        self.effect_layout = effect_layout
     