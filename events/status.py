import discord
import asyncio
import sqlite3
import random
import os

from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class bot_status(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Статус бота на сервере
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = ".help"))
        print("[status.py]:Статус бота активен")
def setup(bot):
    print("status.py ✅")
    bot.add_cog(bot_status(bot))