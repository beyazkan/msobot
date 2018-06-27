import discord
from discord.ext import commands
from help import Help
import youtube_dl
import time
import datetime
import asyncio
from itertools import cycle

times = [
    str(datetime.time(1, 45)), str(datetime.time(15, 35)), str(datetime.time(23, 15))
]

bosses = [
    ['Kzarka', 'Kutum', 'Kzarka'],
    ['Kutum', 'Kzarka', 'Kutum'],
    ['Kzarka', 'Kutum', 'Kzarka'],
    ['Kutum', 'Kzarka', 'Kutum'],
    ['Kzarka', 'Kutum', 'Kzarka'],
    ['Kutum', 'Kzarka', 'Kutum'],
    ['Kzarka', 'Kutum', 'Kzarka']
]

TOKEN = "NDUxMTU5NjczNDA0NjUzNjA4.DfFBtg.hpYRrGhybosK_Wfe16yISuCgiCU"
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

async def alarm():
    await client.wait_until_ready()

    # https://www.youtube.com/watch?v=2CV_Vmh-PGY
    # https://www.youtube.com/watch?v=F9Z21ExXiz8

    while not client.is_closed:
        now = datetime.datetime.now()
        moment = now.time().strftime('%H:%M:%S')
        saat = time.localtime(time.time())
        if times[0] == moment:
            boss = 0
        elif times[1] == moment:
            boss = 1
        else:
            boss = 2

        # print("Saat: {} Dakika: {}".format(saat.tm_hour, saat.tm_min))
        if moment in times:
            print(bosses[saat.tm_wday][boss] + ": 15 dakika içinde çıkacak")
            general_channel = get_channel(client.get_all_channels(), '●sohbet')
            voice_channel = get_channel(client.get_all_channels(), '●Genel Sohbet-1')
            server = get_server(client.servers, 'DRAGON')
            await client.send_message(general_channel, bosses[saat.tm_wday][boss] + ": 15 dakika içinde çıkacak")
            await client.join_voice_channel(voice_channel)
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=2CV_Vmh-PGY')
            players[server.id] = player
            player.start()
            await asyncio.sleep(22)
            voice_client = client.voice_client_in(server)
            await  voice_client.disconnect()
        await asyncio.sleep(1)


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

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await  voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
    while player.is_playing():
        await asyncio.sleep(1)
        if player.is_done():
            voice_client = client.voice_client_in(server)
            await  voice_client.disconnect()


@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()


@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()


client.loop.create_task(alarm())
client.run(TOKEN)
