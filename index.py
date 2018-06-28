import discord
from discord.ext import commands
from help import Help
import os

TOKEN = os.environ.get('BOT_TOKEN')
BOT_PREFIX = "!"

client = commands.Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

players = {}


def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            return channel
    return None


def get_server(servers, server_name):
    for server in servers:
        if server.name == server_name:
            return server
    return None


@client.event
async def on_ready():
    print("Bot çevrimiçi")
    print("İsim: {}".format(client.user.name))
    print("ID : {}".format(client.user.id))
    print(str(len(client.servers)) + " tane serverda çalışıyor.")
    print(str(len(set(client.get_all_members()))) + " tane kullanıcıya erişiyor.")

    await client.change_presence(game=discord.Game(name='Doktorculuk'))


# Todo: Varsayılan Rolü belirleme
# @client.event
# async def on_member_join(member):
#     role = discord.utils.get(member.server.roles, name="Deneme")
#     await  client.add_rules(member, role)

@client.command()
async def ping():
    await client.say('Pong!')


@client.command(pass_context=True)
async def echo(ctx, *args):
    output = ''

    for word in args:
        output += word
        output += ' '

    await client.say(output)


@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []

    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)

    await client.delete_messages(messages)
    await client.say('Eski mesajlar temizlendi.')


@client.command(pass_context=True)
async def help():
    yardim = Help()
    await client.say(yardim.mesaj)


@client.command()
async def logout():
    await client.logout()

client.run(TOKEN)
