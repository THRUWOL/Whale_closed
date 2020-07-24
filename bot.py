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

extensions = [
    'setting.db',
    'setting.configs',
    'events.status',
    'events.xp',
    'events.roles_reaction',
    'commands.admin_commands',
    'commands.moderator_commands',
    'commands.user_commands',
    'games.rps',
    'games.rpg',
    'commands.random_smth']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

print("bot.py ✅")
print("~~~Кит поплыл~~~")
client.run(token.TOKEN)