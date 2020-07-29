from abc import ABC, abstractmethod

import re

class MatchType(ABC):
    @property
    @abstractmethod
    def db_name(self) -> str:
        return ''

    @abstractmethod
    def make_regex(self, phrase: str) -> str:
        return ''

class WordMatchType(MatchType):
    db_name = 'word'

    def make_regex(self, phrase):
        return r'\b'+re.escape(banned_phrase)+r'\b'

class WordPartMatchType(MatchType):
    db_name = 'word_part'

    def make_regex(self, phrase):
        return re.escape(phrase)

class RegexMatchType(MatchType):
    db_name = 'regex'

    def make_regex(self, phrase):
        return self

_MATCH_TYPES = [
    WordMatchType(),
    WordPartMatchType(),
    RegexMatchType()
]

_MATCH_TYPES = {match_type.db_name: match_type for match_type in _MATCH_TYPES}

def get_match_type(db_name):
    return _MATCH_TYPES[db_name]
