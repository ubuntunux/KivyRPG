from kivy.logger import Logger
from utility.singleton import SingletonInstance
from .game_resource import GameResourceManager

class ActorManager(SingletonInstance):
    def __init__(self, app):
        self.app = app