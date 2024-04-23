from typing import TypedDict, NamedTuple

class BaseCallback(NamedTuple):
    cb_processor: str
    cb_type: str

class WordCallback(NamedTuple):
    cb_processor: str
    cb_type: str
    word: str