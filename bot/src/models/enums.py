from enum import Enum, auto


class WordLanguage(Enum):
    ru = auto()
    en = auto()

    def get_description(self):
        if self == WordLanguage.ru:
            return "Русский"
        if self == WordLanguage.en:
            return "Английский"


class WordLevel(Enum):
    A1 = auto()
    A2 = auto()
    A3 = auto()

    def get_description(self):
        if self == WordLevel.A1:
            return "Начальный"
        if self == WordLevel.A2:
            return "Средний"
        if self == WordLevel.A3:
            return "Продвинутый"
