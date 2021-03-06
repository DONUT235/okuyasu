from abc import ABC, abstractmethod
from utilities import clean_string

class Command(ABC):
    _COMMANDS = {}
    needs_guild = False

    @property
    @abstractmethod
    def help_line(self) -> str:
        return ''

    @property
    @abstractmethod
    def name(self) -> str:
        return ''

    @abstractmethod
    async def execute(self, message):
        pass

    def get_args(self, message, lower=True):
        messy_args = message.clean_content[len(f'okuyasu {self.name} '):]
        return clean_string(messy_args, lower=lower)

    def format_help_line(self):
        return f'okuyasu {self.name}: {self.help_line}'

class NeedsGuildCommand(Command):
    needs_guild = True
