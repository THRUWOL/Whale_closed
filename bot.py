import discord
import asyncio
import sqlite3
import random
import os

import config

from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag

client = commands.Bot(command_prefix = config.PREFIX)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = ".help"))
    print("[bot_status]:Статус бота активен")

extensions = ['command','roles_reaction','db','rps','rpg','xp']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

print("bot.py ✅")
print("~~~Кит поплыл~~~")
client.run(config.TOKEN)