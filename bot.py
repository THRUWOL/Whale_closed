import discord
import os
from discord.ext import commands
from discord.utils import get


bot = commands.Bot(command_prefix='.')

# Проверка работоспособности в консоли
@bot.event
async def on_ready():
    print('[log]буль')

# Проверка работоспособности
@bot.command(pass_context=True)
async def bot(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('буль')

# Токен, который находится подальше от чужих глаз
token = os.environ.get('BOT_TOKEN')

# Запуск бота
bot.run(token)
