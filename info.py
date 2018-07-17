import discord
from discord.ext import commands
import database

veritabani = database.Database()
servers = veritabani.server_query_all()

class info:
    def __init__(self, client):
        self.client = client

    """async def on_message_delete(self, message):
        await self.client.send_message(message.channel, 'Mesaj silindi.')"""

    @commands.command()
    async def running_servers(self):
        for server in servers:
            await self.client.say(server[1])


def setup(client):
    client.add_cog(info(client))