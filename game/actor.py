from kivy.logger import Logger
from utility.singleton import SingletonInstance
from .game_resource import GameResourceManager
from .character import Character
from .constant import *

class ActorManager(SingletonInstance):
    def __init__(self, app):
        self.app = app
        self.actors = []
        self.player = None
        
    def initialize(self):
        pass
        
    def get_player(self):
        return self.player
        
    def clear_actors(self):
        for actor in self.actors:
            actor.parent.remove_widget(actor)
        self.actors.clear()
        
    def create_actors(self, parent_widget):
        is_player = True
        character_data = GameResourceManager.instance().get_character_data("player")  
        character = Character(
            character_data=character_data,
            pos=(0,0),
            size=(TILE_SIZE, TILE_SIZE),
            is_player=is_player
        )
        parent_widget.add_widget(character)
        if is_player:
            self.player = character
        self.actors.append(character)
    
    def update(self, dt):
        for actor in self.actors:
            actor.update(dt)
    
        