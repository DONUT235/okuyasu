import discord
import os
import re

from db import db

client = discord.Client()

@client.event
async def on_ready():
    await db.get_connection()

OKUYASU_HELP = """```okuyasu delete <n>: Delete the <n> most recent messages in this channel.
okuyasu ban <phrase>: Ban a phrase.
okuyasu unban <phrase>: Make a phrase legal.
okuyasu ban_containing: Ban a sequence of letters, even if it occurs in the middle of a word.
okuyasu ban_regex: Delete all messages matching a Python-flavored regular expression```"""
BAN_COMMANDS = set(('ban', 'ban_containing', 'ban_regex'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if is_okuyasu_command(message):
        split_content = message.clean_content.lower().split()
        if len(split_content) < 2:
            return
        if split_content[1] == 'help':
            await message.channel.send(OKUYASU_HELP)
        elif split_content[1] == 'delete':
            try:
                num_to_delete = int(split_content[2])
            except (IndexError, ValueError):
                pass
            await delete_n_previous(message, num_to_delete)
        elif split_content[1] in BAN_COMMANDS and len(split_content) > 2:
            await handle_ban_command(message, command=split_content[1])

        elif split_content[1] == 'unban' and len(split_content) > 2:
            await handle_unban_command(message)
    else:
        await handle_moderate_command(message)

async def handle_moderate_command(message):
    if message.guild is not None:
        server_id = str(message.guild.id)
        for banned_phrase in await db.get_banned_phrases_for_server(server_id):
            pattern = makeRegex(
                banned_phrase['match_type'],
                banned_phrase['value'])
            if re.search(
                    pattern,
                    clean(message.clean_content):
                await message.delete()
                await message.channel.send(
                    file=discord.File('assets/ideletedthispost.jpg'))
                return

def clean(content):
    return content.strip().lower()

def getMatchType(command):
    if command == 'ban':
        return 'word'
    elif command == 'ban_containing':
        return 'word_part'
    elif command == 'ban_regex':
        return 'regex'
    else:
        return 'word'

def makeRegex(match_type, banned_phrase):
    if match_type == 'word_part':
        return re.escape(banned_phrase)
    if match_type == 'regex':
        return banned_phrase
    else:
        return r'\b'+re.escape(banned_phrase)+r'\b'

async def handle_ban_command(message, command='ban'):
    if message.guild is not None:
        messy_phrase = message.content[len(f'okuyasu {command} '):]
        phrase_to_ban = clean(messy_phrase)

        match_type = getMatchType(command)

        await db.ban_phrase(
            str(message.guild.id),
            phrase_to_ban,
            match_type=match_type)

        await message.channel.send(
            f'The phrase "{phrase_to_ban}" is now banned.')

async def handle_unban_command(message):
    if message.guild is not None:
        messy_phrase_to_unban = message.clean_content[len('okuyasu unban '):]
        phrase_to_unban = clean(messy_phrase_to_unban)

        await db.unban_phrase(
            str(message.guild.id),
            phrase_to_unban)

        await message.channel.send(
            f'The phrase "{clean(phrase_to_unban)}" is now unbanned.')

def is_okuyasu_command(message):
    #TODO Check for user privileges
    if message.content.lower().startswith('okuyasu'):
        author = message.author
        if author.permissions_in(message.channel).administrator:
            return True
    return False


async def delete_n_previous(message, num_to_delete):
    channel = message.channel
    async for prev_message in channel.history(
        before=message, limit=num_to_delete):
            await prev_message.delete()
    await message.delete()
    await channel.send(file=discord.File('assets/hando.jpg'))
    await channel.send(file=discord.File('assets/thankme.jpg'))

if __name__ == '__main__':
    client.run(os.getenv("OKUYASU_TOKEN"))
