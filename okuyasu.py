import os
import discord
from db import db

client = discord.Client()

@client.event
async def on_guild_join(guild):
    #TODO Create Server Entry for this server.
    await db.create_server(str(guild.id))

OKUYASU_HELP = """```okuyasu delete <n>: Delete the <n> most recent messages in this channel.
okuyasu ban <phrase>: Ban a phrase.
okuyasu unban <phrase>: Make a phrase legal.```"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('okuyasu'):
        await message.channel.send(OKUYASU_HELP)


if __name__ == '__main__':
    client.run(os.getenv("OKUYASU_TOKEN"))
