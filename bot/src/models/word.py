from dataclasses import dataclass

@dataclass
class Word:
    
    word_id: int
    language: str
    level: str
    word: str
    
    def __init__(self, word_id, language, level, word):
        self.word_id=word_id
        self.language=language
        self.level=level
        self.word=word
        
    