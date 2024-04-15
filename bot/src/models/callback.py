from typing import TypedDict

class BaseCallback(TypedDict):
    cb_processor: str
    cb_type: str
    
class QuestionCallback(BaseCallback):
    num_of_question: int
    correct_answer: str