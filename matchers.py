from abc import ABC, abstractmethod

import re

import db_names

class Matcher(ABC):
    def __init__(self, phrase):
        self.phrase = phrase

    @abstractmethod
    async def matches(self, text) -> bool:
        return False

class RegexMatcherTemplate(Matcher):
    @abstractmethod
    def make_regex(self, phrase: str) -> str:
        return ''

    async def matches(self, text):
        return bool(re.search(self.make_regex(), text))

class WholeWord(RegexMatcherTemplate):
    def make_regex(self):
        return r'\b'+re.escape(self.phrase)+r'\b'

class WordPart(RegexMatcherTemplate):
    def make_regex(self):
        return re.escape(self.phrase)

class Regex(RegexMatcherTemplate):
    def make_regex(self):
        return self.phrase

_MATCH_TYPES = {
    db_names.WHOLE_WORD: WholeWord,
    db_names.WORD_PART: WordPart,
    db_names.REGEX: Regex
}

def get_matcher(match_type, value):
    return _MATCH_TYPES[match_type](value)
