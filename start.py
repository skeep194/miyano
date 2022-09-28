import discord
from discord.ext import commands
import json
import service
from conf import conf
from er_request import get_request
import miyano_user
import datetime

bot = commands.Bot(command_prefix='/', help_command=None, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'실험용 디스코드 봇 {bot.user}')

@bot.command()
async def say(message):
    await message.reply(str(message.author.name)+f' {arg1} {arg2}왈랄랄랄루~~~~~~')

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
    user_num = service.get_user_num(user_str)
    req = get_request(f'user/games/{user_num}')
    res = service.get_game_data(req["userGames"][0]["gameId"])
    await message.send(res)

@bot.command()
async def game(message, arg):
    await message.send(service.get_game_data(arg))

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

bot.run(conf["discord-token"])