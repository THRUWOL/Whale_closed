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

class server_config(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Установка ID для реакции
    @commands.command()
    async def rm_id(self,ctx, id = None):
        cursor.execute(f"UPDATE config SET reaction_message_id = {id} WHERE server_ID = {ctx.author.guild.id}")
        connection.commit()
        await ctx.send(f"ID сообщения под реакции установлено")
# Установка ID для rpg
    @commands.command()
    async def rpg_id(self,ctx, id = None):
        cursor.execute(f"UPDATE config SET rpg_id = {id} WHERE server_ID = {ctx.author.guild.id}")
        connection.commit()
        await ctx.send(f"ID канала под rpg установлено")
# Установка Id для rps
    @commands.command()
    async def rps_id(self,ctx, id = None):
        cursor.execute(f"UPDATE config SET rps_id = {id} WHERE server_ID = {ctx.author.guild.id}")
        connection.commit()
        await ctx.send(f"ID канала под rps установлено")
def setup(bot):
    print("configs.py ✅")
    bot.add_cog(server_config(bot))