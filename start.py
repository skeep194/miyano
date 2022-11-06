import discord
from discord.ext import commands
import json
import service
from request.er_request import get_request
import request.get_data
import user.miyano_user as miyano_user
from result_image.cobalt import get_cobalt_image
import datetime
from conf import conf

bot = commands.Bot(command_prefix='/', help_command=None, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'실험용 디스코드 봇 {bot.user}')

@bot.command()
async def say(message):
    await message.reply('왈랄랄랄루~~~~~~')

@bot.command()
async def 전역(message):
    await message.send(str((datetime.date(2023, 8, 7)-datetime.date.today()).days) + "ㅠㅠㅠ")

@bot.command()
async def recent(message, *arg):
    if len(arg) == 0:
        try:
            user_str = miyano_user.get_er_nickname(message.author.id)
        except:
            await message.send('등록되지 않은 사용자입니다. /register 명령어를 통해 이터널 리턴 닉네임을 등록해주세요.')
            return
    elif len(arg) == 1:
        user_str = arg[0]
    user_num = request.get_data.get_user_num(user_str)
    req = request.get_data.get_user_game(user_num)
    service.get_game_data(req[0]["gameId"], "image")
    with open('/root/Miyano/temp_image/temp.png', 'rb') as f:
        await message.send(file=discord.File(f))

@bot.command()
async def game(message, arg):
    service.get_game_data(arg, "image")
    with open('/root/Miyano/temp_image/temp.png', 'rb') as f:
        await message.send(file=discord.File(f))

@bot.command()
async def register(message, er_nickname):
    ret = miyano_user.register(message.author.id, er_nickname)
    msg = f'{message.author.name}(discord) - {er_nickname}(ER) 등록 완료'
    if not ret:
        msg = '등록 실패'
    await message.send(msg)

@bot.command()
async def failnote(message):
    with open("/root/Miyano/document/failnote", 'r') as f:
        await message.send(str(f.read()))

@bot.command()
async def help(message):
   with open("/root/Miyano/document/help", 'r') as f:
       await message.send(str(f.read()))

@bot.command()
async def debug(message, arg):
    req = get_request(f'games/{arg}')
    get_cobalt_image(req['userGames'], 'temp')
    with open('/root/Miyano/temp_image/temp.png', 'rb') as f:
        await message.send(file=discord.File(f))


bot.run(conf["discord-token"])