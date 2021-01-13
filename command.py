from abc import ABC, abstractmethod
from db import db
from utilities import clean_string, format_regex

import asyncio
import discord
import db_names

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

class KillCommand(Command):
    help_line = 'Delete ALL messages sent by <user>'
    name = 'kill'

    async def execute(self, message):
        username = self.get_args(message)
        server_id = message.guild.id
        if not db.can_kill(str(server_id)):
            await channel.send('No.')
            return
        delete_jobs = []
        for text_channel in message.guild.channels:
            if not isinstance(text_channel, discord.TextChannel):
                pass
            async for prev_message in text_channel.history():
                name = prev_message.author.name
                discriminator = prev_message.author.discriminator
                #TODO Verify This Works
                if f'{name}#{discriminator}' == username:
                    delete_jobs.append(prev_message.delete())
        channel = message.channel
        await asyncio.gather(message.delete(), 
                             db.disable_kill(server_id),
                             *delete_jobs)
        await channel.send(file=discord.File('assets/hando.jpg'))
        await channel.send(file=discord.File('assets/ideletedthisuser.jpg'))


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

class WhatsBannedCommand(NeedsGuildCommand):
    name = 'banlist'
    help_line = 'DM you a list of the banned words for this server'

    async def execute(self, message):
        server_id = message.guild.id
        banned_phrases = await db.get_banned_phrases_for_server(server_id)
        banned_dict = {}
        for phrase in banned_phrases:
            if phrase['match_type'] not in banned_dict:
                banned_dict[phrase['match_type']] = []
            banned_dict[phrase['match_type']].append(phrase['value'])
        response = []
        for key in banned_dict:
            if key == db_names.WHOLE_WORD:
                response.append('The following phrases are banned:')
            elif key == db_names.WORD_PART:
                response.append(
                    'The following phrases are banned'
                    + ', even if they occur in the middle of a word:')
            elif key == db_names.REGEX:
                response.append(
                    'Messages matching the following regex patterns'
                    + ' will be deleted:')
                banned_dict[key] = [
                    format_regex(phrase)
                    for phrase in banned_dict[key]
                ]
            response.extend(banned_dict[key])

        sender = message.author
        if(response):
            await message.author.send('\n'.join(response))
        else:
            await message.author.send('Nothing is currently banned.')


class BanCommand(NeedsGuildCommand):
    @property
    @abstractmethod
    def db_name(self) -> str:
        return None

    async def execute(self, message):
        server_id = message.guild.id
        phrase_to_ban = self.get_args(message)
        if phrase_to_ban == '':
            #This is potentially dangerous!
            return
        await db.ban_phrase(
            str(server_id), phrase_to_ban, self.db_name)

        await message.channel.send(
            f'The phrase {self.format(phrase_to_ban)} is now banned.')

    def format(self, phrase):
        return '"' + phrase + '"'

class BanRegexCommand(BanCommand):
    help_line = 'Delete all messages matching a Python-flavored regular expression.'
    name = 'ban_regex'
    db_name = db_names.REGEX

    def format(self, phrase):
        return format_regex(phrase)

class BanContainingCommand(BanCommand):
    help_line = 'Ban a sequence of letters, even if it occurs in the middle of a word.'
    name = 'ban_containing'
    db_name = db_names.WORD_PART

class BanWordCommand(BanCommand):
    help_line = 'Ban a phrase.'
    name = 'ban'
    db_name = db_names.WHOLE_WORD

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
    BanWordCommand(),
    UnbanCommand(),
    WhatsBannedCommand()
]

_COMMANDS = {command.name: command for command in _COMMANDS}

def get_command(commandName):
    if commandName in _COMMANDS:
        return _COMMANDS[commandName]
    else:
        return NullCommand()
