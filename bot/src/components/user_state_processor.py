from enum import Enum, auto

class UserStateProcessor:
    
    class State(Enum):
        lesson_active = auto()
        lesson_inactive = auto()
    
    def set_state(self, user_id, state):
        pass
    
    def get_state(self, user_id) -> State:
        pass
    
    def set_data(self, user_id, data):
        pass
    
    def get_data(self, user_id) -> dict:
        pass