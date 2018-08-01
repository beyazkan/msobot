import config
import database
import discord
from discord.ext import commands
import asyncio
import json

veritabani = database.Database()
client = commands.Bot(command_prefix=config.BOT_PREFIX)
extensions = ["fun","info"]
server_ids = list()
servers = veritabani.server_query_all()
member_ids = list()
members = veritabani.uye_query_all()

banlist = [451159673404653608, 235088799074484224, 429613776380100615, 201503408652419073]
yetkililer = [int(config.YETKILI_1), int(config.YETKILI_2), int(config.YETKILI_3)]

bot_banlayanlar = list()

def yetkili_atama():
    server = client.get_server(int(config.SERVER_ID))
    for yetki in yetkililer:
        yetkiler = server.get_member(str(yetki))

def server_kayit():
    for i in servers:
        server_ids.append(int(i[0]))

    for svr in client.servers:
        if not int(svr.id) in server_ids:
            liste = list()
            liste.append(svr.id)
            liste.append(svr.name)
            veritabani.server_insert(liste)
            servers.append(liste)
            print("{} adlı yeni server eklendi.".format(svr.name))

def serverlar():
    print('Aktif Sunucular - {}'.format(len(servers)));
    for server in servers:
        print('ID: {} Adı: {}'.format(server[0], server[1]))

def uye_kayit():
    for i in members:
        member_ids.append(int(i[1]))

    for server in client.servers:
        for member in server.members:
            if not int(member.id) in member_ids:
                if not int(member.id) in banlist:
                    liste = list()
                    liste.append(member.id)
                    liste.append(member.name.strip())
                    liste.append(server.id)
                    members.append(liste)
                    veritabani.uye_insert(liste)

def uyeler():
    for member in members:
        print(member[1])

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id='430347017642835969')
    while not client.is_closed:
        counter += 1
        #await client.send_message(channel, counter)
        await asyncio.sleep(60) # task runs every 60 seconds

@client.event
async def on_ready():
    print("Bot çevrimiçi")
    print("İsim: {}".format(client.user.name))
    print("ID : {}".format(client.user.id))
    print(str(len(client.servers)) + " tane serverda çalışıyor.")
    print(str(len(set(client.get_all_members()))) + " tane kullanıcıya erişiyor.")
    server_kayit()
    serverlar()
    uye_kayit()
    #uyeler()
    #yetkili_atama()

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

@client.command()
async def logout():
    await client.logout()

@client.command(pass_context=True) # Here we are getting the member object
async def duyuru(ctx, *args):
    server = ctx.message.server

    if int(ctx.message.author.id) in yetkililer:
        output = ''

        for word in args:
            output += word
            output += ' '

        for user in members:
            if int(ctx.message.server.id) == int(user[3]):
                user_id = server.get_member(str(user[1]))
                if config.PERM in [y.name.lower() for y in user_id.roles]:
                    try:
                        await client.send_message(user_id, output)
                        print("{} adlı kullanıcıya mesaj gönderildi.".format(user_id))
                        await asyncio.sleep(int(config.DUYURU_SURESI))  # task runs every 10 seconds
                    except (discord.errors.Forbidden, discord.ext.commands.errors.CommandInvokeError):
                        liste = list()
                        liste.append(user[1])
                        liste.append(user[2])
                        bot_banlayanlar.append(liste)
                        print("Banlayan Kullanıcı: " + user[2])
                        continue

    else:
        await client.say('Bu işlemi kullanmak için yetkiniz yok.')

# Botu banlayan kişilerin listelemesini gerçekleştirme
@client.command(pass_context=True)
async def bot_banlayan(ctx):
    output = ''
    for user in bot_banlayanlar:
        output += str(user[0]) + ' - ' + str(user[1]) + ',\n'
    output += "Lütfen bu kişiler ile görüşme sağlayıp, banlarını kaldırmalarını rica edin."

    await client.say(output)

@client.command()
async def load(extension):
    try:
        client.load_extension(extensions)
        print('{} eklenti yüklendi'.format(extensions))
    except Exception as error:
        print('{} eklentisi yüklenemedi. [{}]'.format(extensions, error))

@client.command()
async def unload(extension):
    try:
        client.unload_extension(extensions)
        print('{} eklenti kaldırıldı.'.format(extensions))
    except Exception as error:
        print('{} eklentisi yüklenemedi. [{}]'.format(extensions, error))


if __name__ == '__main__':
    for extensions in extensions:
        try:
            client.load_extension(extensions)
        except Exception as error:
            print('{} eklentisi yüklenemedi. [{}]'.format(extensions, error))

    #client.loop.create_task(my_background_task())
    client.run(config.TOKEN)
