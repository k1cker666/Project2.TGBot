from typing import TypedDict

class Callback(TypedDict):
    cb_processor: str
    cb_type: str
    num_of_question: int
    correct_answer: str
