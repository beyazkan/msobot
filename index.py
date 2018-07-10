import discord
from discord.ext import commands
from help import Help
import json
import os

TOKEN = os.environ.get('BOT_TOKEN')
BOT_PREFIX = "_"

client = commands.Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.event
async def on_ready():
    print("Bot çevrimiçi")
    print("İsim: {}".format(client.user.name))
    print("ID : {}".format(client.user.id))
    print(str(len(client.servers)) + " tane serverda çalışıyor.")
    print(str(len(set(client.get_all_members()))) + " tane kullanıcıya erişiyor.")

    await client.change_presence(game=discord.Game(name='Doktorculuk'))

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

@client.event
async def on_member_join(member):
    with open('user.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    with open('user.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)


async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel, '{} adlı üyemiz, {} seviyesine yükseldi.'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end

client.run(TOKEN)
