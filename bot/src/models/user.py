from dataclasses import dataclass
from src.models.enums import WordLanguage

@dataclass
class User:
    
    user_id: int
    tg_login: str
    login: str
    password: str
    words_in_lesson: int
    native_language: WordLanguage
    language_to_learn: WordLanguage
    
    def __init__(self,
                user_id: str,
                tg_login: str,
                login: str,
                password: str,
                words_in_lesson: int,
                native_language: str,
                language_to_learn: str):
        
        self.user_id = user_id
        self.tg_login = tg_login
        self.login = login
        self.password = password
        self.words_in_lesson = words_in_lesson
        self.native_language = WordLanguage[native_language]
        self.language_to_learn = WordLanguage[language_to_learn]