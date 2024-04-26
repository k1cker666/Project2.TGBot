from src.components.lesson_dto import LessonDTO, Question

class LessonInitProcessor:
    
    def __init__(self) -> None:
        pass
    
    def init(self) -> LessonDTO:
        questions = [
            Question(
                id = 1,
                word_to_translate = 'word_A',
                answers = ['A', 'B', 'C', 'D'],
                correct_answer = 'A'
            ),
            Question(
                id = 2,
                word_to_translate = 'word_B',
                answers = ['A', 'B', 'C', 'D'],
                correct_answer = 'B'
            )
        ]
        return LessonDTO(questions=questions)
