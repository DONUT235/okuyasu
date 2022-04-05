from command.base import Command, NeedsGuildCommand
from db import db

import asyncio
import discord

class DeleteNCommand(Command):
    display_name = 'delete <n>'
    help_line = 'Delete the <n> most recent messages in this channel.'
    name = 'delete'

    async def execute(self, message):
        num_to_delete = self.get_args(message)
        try:
            num_to_delete = int(num_to_delete)
        except (IndexError, ValueError):
            return

        channel = message.channel
        delete_jobs = []
        async for prev_message in channel.history(
            before=message, limit=num_to_delete
        ):
            delete_jobs.append(prev_message.delete())

        await asyncio.gather(message.delete(), *delete_jobs)
        await channel.send(file=discord.File('assets/hando.jpg'))
        await channel.send(file=discord.File('assets/thankme.jpg'))

class KillCommand(NeedsGuildCommand):
    help_line = 'Delete ALL messages sent by <user>'
    name = 'kill'
    display_name = 'kill <user>'

    async def execute(self, message):
        username = self.get_args(message, lower=False)
        server_id = message.guild.id
        channel = message.channel
        if not await db.can_kill(server_id):
            await channel.send('No.')
            return
        else:
            await channel.send('OK!')
        deleted_any = False
        for text_channel in message.guild.channels:
            try:
                if text_channel.type != discord.ChannelType.text:
                    continue
                async for prev_message in text_channel.history(limit=None):
                    name = prev_message.author.name
                    discriminator = prev_message.author.discriminator
                    #TODO Verify This Works
                    if f'{name}#{discriminator}' == username:
                        await prev_message.delete()
                        deleted_any = True
            except discord.DiscordException:
                pass

        if deleted_any:
            await db.disable_kill(server_id)
            await channel.send(file=discord.File('assets/hando.jpg'))
            await channel.send(file=discord.File('assets/ideletedthisuser.jpg'))
        else:
            await channel.send("I couldn't find anything."
                               + " Usernames must match EXACTLY,"
                               + " including the # and the"
                               + " 4 numbers after it.")
