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

class kfc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Запуск игры "Быки и коровы"
    @commands.command()
    async def bc(self):
        pass
def setup(bot):
    print("bulls_and_cows.py ✅")
    bot.add_cog(kfc(bot))