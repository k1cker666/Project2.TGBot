from typing import TypedDict, NamedTuple

class BaseCallback(NamedTuple):
    cb_processor: str
    cb_type: str

class WordCallback(NamedTuple):
    cb_processor: str
    cb_type: str
    word: str
    
class Data(TypedDict):
    state: str
    num_of_question: int
    correct_answer: str