from command.base import Command, NeedsGuildCommand
from db import db

import asyncio
import discord

class DeleteNCommand(Command):
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

    async def execute(self, message):
        username = self.get_args(message, lower=False)
        server_id = str(message.guild.id)
        channel = message.channel

        if not await db.can_kill(server_id):
            await channel.send('No.')
            return

        delete_jobs = []
        for text_channel in message.guild.channels:
            try:
                if text_channel.type != discord.ChannelType.text:
                    continue

                async for prev_message in text_channel.history():
                    name = prev_message.author.name
                    discriminator = prev_message.author.discriminator
                    if f'{name}#{discriminator}' == username:
                        delete_jobs.append(prev_message.delete())

            except discord.DiscordException:
                pass

        if(len(delete_jobs) > 0):
            await asyncio.gather(db.disable_kill(server_id),
                                 *delete_jobs)
            await channel.send(file=discord.File('assets/hando.jpg'))
            await channel.send(
                file=discord.File('assets/ideletedthisuser.jpg')
            )

        else:
            await channel.send("I couldn't find anything."
                               " Usernames must match EXACTLY,"
                               " including the # and the"
                               " 4 numbers after it.")
