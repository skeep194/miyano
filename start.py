import discord
from discord.ext import commands
import requests
import json
import service
from conf import conf


bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'실험용 디스코드 봇 {bot.user}')



@bot.command()
async def say(message):
    await message.reply('왈랄랄랄루~~~~~~')

@bot.command()
async def user(message, arg):
    req = requests.get(conf["endpoint"]+f'user/nickname?query={arg}', headers=conf["header"])
    req = requests.get(conf["endpoint"] + f'user/games/{userNum}', headers=conf["header"])
    await message.send(json.loads(req.text)["userGames"][0]["characterNum"])

@bot.command()
async def recent(message, arg):
    userNum = service.getUserNum(arg)
    req = requests.get(conf["endpoint"]+f'user/games/{userNum}', headers=conf["header"])
    res = service.getCobaltData(json.loads(req.text)["userGames"][0]["gameId"])
    await message.send(res)

@bot.command()
async def game(message, arg):
    await message.send(service.getCobaltData(arg))

bot.run(conf["discord-token"])