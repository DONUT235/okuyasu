from abc import ABC, abstractmethod
from db import db
from utilities import clean_string

import match_type

class Command(ABC):
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

    def get_args(self, message):
        messy_args = message.clean_content[len(f'okuyasu {self.name} '):]
        return clean_string(messy_args)

    def format_help_line(self):
        return f'okuyasu {self.name}: {self.help_line}'

class DeleteNCommand(Command):
    help_line = 'Delete the <n> most recent messages in this channel.'
    name = 'delete'

    async def execute(self, message):
        num_to_delete = self.get_args(message)
        try:
            num_to_delete = int(num_to_delete)
        except (IndexError, ValueError):
            pass

        channel = message.channel
        delete_jobs = []
        async for prev_message in channel.history(
            before=message, limit=num_to_delete):
                delete_jobs.append(prev_message.delete())
        await asyncio.gather(message.delete(), *delete_jobs)
        await channel.send(file=discord.File('assets/hando.jpg'))
        await channel.send(file=discord.File('assets/thankme.jpg'))

class HelpCommand(Command):
    help_line = 'Print this message.'
    name = 'help'

    async def execute(self, message):
        commands = _COMMANDS.values()
        if message.guild is None:
            commands = filter(
                lambda command: not command.needs_guild, 
                commands)
        help_messages = [command.format_help_line() for command in commands]
        help_message = "\n".join(help_messages)
        await message.channel.send(f'```{help_message}```')

class NullCommand(Command):
    help_line = ''
    name = 'null'

    async def execute(self, message):
        pass

class NeedsGuildCommand(Command):
    needs_guild = True

class BanWordInDBCommand(NeedsGuildCommand):
    @property
    @abstractmethod
    def match_type() -> match_type.MatchType:
        return None

    async def execute(self, message):
        server_id = message.guild.id
        phrase_to_ban = self.get_args(message)
        if phrase_to_ban == '':
            #This is potentially dangerous!
            return
        await db.ban_phrase(
            server_id, phrase_to_ban, self.match_type.db_name)

        await message.channel.send(
            f'The phrase "{phrase_to_ban}" is now banned.')

class BanRegexCommand(BanWordInDBCommand):
    help_line = 'Delete all messages matching a Python-flavored regular expression.'
    name = 'ban_regex'
    match_type = match_type.RegexMatchType()

class BanContainingCommand(BanWordInDBCommand):
    help_line = 'Ban a sequence of letters, even if it occurs in the middle of a word.'
    name = 'ban_containing'
    match_type = match_type.WordPartMatchType()

class BanCommand(BanWordInDBCommand):
    help_line = 'Ban a phrase.'
    name = 'ban'
    match_type = match_type.WordMatchType()

class UnbanCommand(NeedsGuildCommand):
    help_line = 'Make a phrase legal.'
    name = 'unban'

    async def execute(self, message):
        phrase_to_unban = self.get_args(message)

        await db.unban_phrase(str(message.guild.id), phrase_to_unban)

        await message.channel.send(
            f'The phrase "{phrase_to_unban}" is now unbanned.')


_COMMANDS = [
    HelpCommand(),
    DeleteNCommand(),
    BanRegexCommand(),
    BanContainingCommand(),
    BanCommand(),
    UnbanCommand()
]

_COMMANDS = {command.name: command for command in _COMMANDS}

def get_command(commandName):
    if commandName in _COMMANDS:
        return _COMMANDS[commandName]
    else:
        return NullCommand()
