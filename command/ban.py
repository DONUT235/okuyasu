from abc import abstractmethod
from command.base import NeedsGuildCommand
from db import db
from utilities import format_regex

import db_names

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
                    + ', even if they occur in the middle of a word:'
                )

            elif key == db_names.REGEX:
                response.append(
                    'Messages matching the following regex patterns'
                    ' will be deleted:'
                )
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
            server_id, phrase_to_ban, self.db_name
        )

        await message.channel.send(
            f'The phrase {self.format(phrase_to_ban)} is now banned.'
        )

    def format(self, phrase):
        return '"' + phrase + '"'

class BanRegexCommand(BanCommand):
    help_line = (
        'Delete all messages matching a Python-flavored regular expression.'
    )
    name = 'ban_regex'
    db_name = db_names.REGEX

    def format(self, phrase):
        return format_regex(phrase)

class BanContainingCommand(BanCommand):
    help_line = (
        'Ban a sequence of letters, even if it occurs in the middle of a word.'
    )
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

        await db.unban_phrase(message.guild.id, phrase_to_unban)

        await message.channel.send(
            f'The phrase "{phrase_to_unban}" is now unbanned.'
        )
