from command.bulk_delete import DeleteNCommand, KillCommand
from command.ban import (
    WhatsBannedCommand,
    BanWordCommand,
    BanContainingCommand,
    BanRegexCommand,
    UnbanCommand
)
from command.base import Command

_COMMANDS = {}

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

def register(*commands):
    for command in commands:
        _COMMANDS[command.name] = command

register(
    HelpCommand(),
    DeleteNCommand(),
    KillCommand(),
    BanWordCommand(),
    BanContainingCommand(),
    BanRegexCommand(),
    WhatsBannedCommand(),
    UnbanCommand(),
)

def get_command(commandName):
    if commandName in _COMMANDS:
        return _COMMANDS[commandName]
    else:
        return NullCommand()
