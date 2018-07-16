import discord
from discord.ext import commands


class Fun:
    def __init__(self, client):
        self.client = client

    """async def on_message_delete(self, message):
        await self.client.send_message(message.channel, 'Mesaj silindi.')"""

    @commands.command()
    async def ping(self):
        await self.client.say('Pong!')


def setup(client):
    client.add_cog(Fun(client))