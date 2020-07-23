import discord
import asyncio
import sqlite3
import random
import os

import setting.token as token

from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

extensions = ['setting.db','events.status','setting.configs','commands.commands','events.roles_reaction','games.rps','games.rpg']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

print("bot.py ✅")
print("~~~Кит поплыл~~~")
client.run(token.TOKEN)