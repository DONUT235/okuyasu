from abc import ABC, abstractmethod

import re

import db_names

class TextMatchStrategy(ABC):
    def __init__(self, phrase):
        self.phrase = phrase

    @property
    @abstractmethod
    def db_name(self) -> str:
        return ''

    @abstractmethod
    def matches(self, text) -> bool:
        return False

class RegexTextMatch(TextMatchStrategy):
    @abstractmethod
    def make_regex(self, phrase: str) -> str:
        return ''

    def matches(self, text):
        return bool(re.search(self.make_regex(), text))

class WholeWord(RegexTextMatch):
    db_name = db_names.WHOLE_WORD

    def make_regex(self):
        return r'\b'+re.escape(self.phrase)+r'\b'

class WordPart(RegexTextMatch):
    db_name = db_names.WORD_PART

    def make_regex(self):
        return re.escape(self.phrase)

class ArbitraryRegex(RegexTextMatch):
    db_name = db_names.REGEX

    def make_regex(self):
        return self.phrase

_MATCH_TYPES = [
    WholeWord,
    WordPart,
    ArbitraryRegex
]

_MATCH_TYPES = {match_type.db_name: match_type for match_type in _MATCH_TYPES}

def get_match_type(db_name, phrase):
    return _MATCH_TYPES[db_name](phrase)
