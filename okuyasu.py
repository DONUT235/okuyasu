import discord
import os
import re
import asyncio

from db import db

from command import get_command
from match_type import get_match_type
from utilities import clean_message, clean_string

client = discord.Client()

@client.event
async def on_connect():
    await db.get_connection()
    
@client.event
async def on_ready():
    print('Connected')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if is_okuyasu_command(message):
        split_content = clean_message(message).split()
        if len(split_content) < 2:
            return
        command_name = split_content[1]
        command = get_command(commandName)
        if message.guild is not None or not command.needs_guild:
            await command.execute(message)
    else:
        await handle_moderate_command(message)

async def handle_moderate_command(message):
    if message.guild is not None:
        server_id = str(message.guild.id)
        for banned_phrase in await db.get_banned_phrases_for_server(server_id):
            match_type = get_match_type(banned_phrase['match_type'])
            pattern = match_type.make_regex()
            if re.search(pattern, clean_message(message)):
                channel = message.channel
                await message.delete()
                await channel.send(
                    file=discord.File('assets/ideletedthispost.jpg'))

def is_okuyasu_command(message):
    #TODO Check for user privileges
    if message.content.lower().startswith('okuyasu'):
        author = message.author
        if author.permissions_in(message.channel).administrator:
            return True
    return False


if __name__ == '__main__':
    client.run(os.getenv("OKUYASU_TOKEN"))
