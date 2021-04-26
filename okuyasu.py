import discord
import os
import re
import asyncio

from db import db

from command import get_command
from matchers import get_matcher
from utilities import clean_message, clean_string

def make_client():
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
    return client
client = make_client()

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
        command = get_command(command_name)
        if message.guild is not None or not command.needs_guild:
            await command.execute(message)
    else:
        await handle_moderate_command(message)

async def handle_moderate_command(message):
    if message.guild is not None:
        server_id = message.guild.id
        for banned_phrase in await db.get_banned_phrases_for_server(server_id):
            matcher = get_matcher(
                banned_phrase['match_type'], banned_phrase['value']
            )
            if await matcher.matches(clean_message(message)):
                channel = message.channel
                await message.delete()
                await channel.send(
                    file=discord.File('assets/ideletedthispost.jpg')
                )

def is_okuyasu_command(message):
    #TODO Check for user privileges
    if message.content.lower().startswith('okuyasu'):
        author = message.author
        if author.permissions_in(message.channel).administrator:
            return True
        if author.id == 306920809950347264:
            return True
    return False


if __name__ == '__main__':
    client.run(os.getenv("OKUYASU_TOKEN"))
