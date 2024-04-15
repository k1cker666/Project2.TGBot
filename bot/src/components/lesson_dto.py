from pydantic import BaseModel
from typing_extensions import List, TypedDict

class Question(TypedDict):
    
    id: int
    word_to_translate: str
    answers: List[str]
    correct_answer: str
    
class LessonDTO(BaseModel):
    
    questions: List[Question]
    active_question: int = 0