import os
import discord
from db import db

client = discord.Client()

@client.event
async def on_ready():
    await db.get_connection()

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

    if is_okuyasu_command(message):
        split_content = message.content.lower().split()
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

def is_okuyasu_command(message):
    #TODO Check for user privileges
    return message.content.lower().startswith('okuyasu')


async def delete_n_previous(message, num_to_delete):
    #TODO get channel of message, get the messages to delete with
    #channel.history(limit=num_to_delete, before=message
    channel = message.channel
    async for prev_message in channel.history(
        before=message, limit=num_to_delete):
            await prev_message.delete()
    await channel.send(file=discord.File('assets/hando.jpg'))
    await channel.send(file=discord.File('assets/thankme.jpg'))

if __name__ == '__main__':
    client.run(os.getenv("OKUYASU_TOKEN"))
