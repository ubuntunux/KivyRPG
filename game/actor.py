from kivy.logger import Logger
from kivy.vector import Vector
from utility.singleton import SingletonInstance
from utility.kivy_helper import *
from .game_resource import GameResourceManager
from .behavior import Monster
from .character import Character
from .constant import *


class ActorManager(SingletonInstance):
    def __init__(self, app):
        self.app = app
        self.level_manager = None
        self.actors = []
        self.player = None
        
    def initialize(self, level_manager):
        self.level_manager = level_manager
        
    def get_player(self):
        return self.player
        
    def clear_actors(self):
        for actor in self.actors:
            actor.parent.remove_widget(actor)
        self.actors.clear()
        
    def create_actors(self, parent_widget):
        is_player = True
        player_pos = (10, 10)
        character_data = GameResourceManager.instance().get_character_data("player")  
        self.create_actor(parent_widget, character_data, player_pos, is_player)
        
        is_player = False
        monster_positions = [(5, 5), (8, 8)]
        character_data = GameResourceManager.instance().get_character_data("monster")  
        for pos in monster_positions:
            self.create_actor(parent_widget, character_data, pos, is_player)   
        
    def create_actor(self, parent_widget, character_data, tile_indices, is_player):
        pos = Vector(tile_indices) * TILE_SIZE
        pos = get_discrete_center(pos, TILE_SIZE)
        character = Character(
            character_data=character_data,
            pos=pos,
            size=TILE_SIZE,
            is_player=is_player
        )
        parent_widget.add_widget(character)
        if is_player:
            self.player = character
        self.actors.append(character)
        
    def callback_touch(self, inst, touch):
        self.get_player().move_to(touch.pos)
    
    def update(self, dt):
        for actor in self.actors:
            actor.update(dt)
    
        