from dataclasses import dataclass
from src.models.enums import WordLanguage, WordLevel

@dataclass
class Word:
    
    word_id: int
    language: WordLanguage
    level: WordLevel
    word: str
    
    def __init__(self, word_id: str, language: str, level: str, word: str):
        self.word_id=word_id
        self.language=WordLanguage[language]
        self.level=WordLevel[level]
        self.word=word