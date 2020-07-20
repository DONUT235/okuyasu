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
        elif split_content[1] == 'ban' && len(split_content) > 2:
            await handle_ban_command(message)

        elif split_content[2] == 'unban' && len(split_content) > 2:
            await handle_unban_command(message)
    else:
        await handle_moderate_command(message)

async def handle_moderate_command(message):
    if message.guild is not None:
        server_id = str(message.guild.id)
        banned_phrases = await get_banned_phrases_for_server(server_id)

async def handle_ban_command(message):
    if message.guild is not None:
        phrase_to_ban = message.content[len('okuyasu ban '):].strip().lower()

        await db.ban_phrase(
            message.guild.id, 
            phrase_to_ban)

        await message.channel.send(
            f'The phrase `{phrase_to_ban}` is now banned.')


async def handle_unban_command(message):
    if message.guild is not None:
        messy_phrase_to_unban = message.content[len('okuyasu unban '):]
        phrase_to_unban = messy_phrase_to_unban.strip().lower()

        await db.unban_phrase(
            message.guild.id,
            phrase_to_unban)

        await message.channel.send(
            f'The phrase `{phrase_to_unban}` is now unbanned.'.)

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
