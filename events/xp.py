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

class xp_events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Выдача уровня за сообщение
    @commands.Cog.listener()
    async def on_message(self,message):
        if len(message.content) > 10:
            for row in cursor.execute(f"SELECT exp, lvl, cash FROM users WHERE id = {message.author.id}"):
                if cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0] == 15:
                    expi = row[0]+20
                elif cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0] == -5:
                    expi = row[0]+5
                elif cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0] == -228:
                    expi = row[0]+0
                else:
                    expi = row[0]+10
                cursor.execute(f"UPDATE users SET exp = {expi} WHERE id = {message.author.id}")
                lvch = expi/(row[1]*100)
                lv = int(lvch)
                if row[1] < lv:
                    await message.channel.send(f"**{message.author.name}** получает новый уровень <a:Cheers:733731087515123832>")
                    bal = 1000*lv
                    cursor.execute(f"UPDATE users SET lvl={lv}, cash= cash +{bal} where id = {message.author.id}")
                    print(f"[lvl_up]:[{message.author.name}] получил уровень {lv}")
        connection.commit()
def setup(bot):
    print("xp.py ✅")
    bot.add_cog(xp_events(bot))