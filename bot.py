'''
Python bot for Discord
last update: 15 may 2020

by Nikita [thruwol] Yarosh
'''
import discord
import os
from discord.ext import commands
from discord.utils import get

# создание клиента discord
client = discord.Client()

# префикс для команд боту
bot = commands.Bot(command_prefix='.')

# взятие токена с спец. сервиса
token = os.environ.get('BOT_TOKEN')

# вывод информации о боте в log
@client.event
async def on_ready():
    try:
        print('i am alive')
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))
        print('_________________')

    except Exception as e:
        print(e)

# добавление новых сообщений
@client.event
async def on_message(message):
    #ввод сообщения
    await message.channel.send('Hello!')

# запуск бота
client.run(token)
