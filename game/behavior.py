from enum import Enum
import random
from kivy.vector import Vector


class BehaviorState(Enum):
    IDLE = 0
    ROAMING = 1
    TRACE_TARGET = 2


class Behavior:
    def __init__(self, actor):
        self.actor = actor
        self.behavior_state = BehaviorState.IDLE
        self.behavior_time = -1
        
    def is_behavior_state(self, behavior_state):
        return behavior_state == self.behavior_state
    
    def get_behavior_state(self):
        return self.behavior_state
    
    def set_behavior_state(self, behavior_state, behavior_time=1.0):
        self.behavior_state = behavior_state
        self.behavior_time = behavior_time
    
    def update_behavior(self, actor_manager, level_manager, dt):
        pass


class Player(Behavior):
    pass


class Monster(Behavior):
    def set_behavior_state(self, behavior_state, behavior_time=1.0):
        super().set_behavior_state(behavior_state, behavior_time)
        if behavior_state == BehaviorState.ROAMING:
            pass
    
    def update_behavior(self, actor_manager, level_manager, dt):
        super().update_behavior(actor_manager, level_manager, dt)
        is_behavior_done = self.behavior_time < 0
        if self.is_behavior_state(BehaviorState.IDLE):
            if is_behavior_done:
                self.set_behavior_state(BehaviorState.ROAMING)
        elif self.is_behavior_state(BehaviorState.ROAMING):
            if is_behavior_done:
                self.set_behavior_state(BehaviorState.IDLE)
        
        if self.actor.get_updated_tile_pos():
            tile_pos = actor_manager.get_player().get_tile_pos()
            self.actor.move_to(level_manager, tile_pos)
        self.behavior_time -= dt
            