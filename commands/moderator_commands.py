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

class moderator_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Очистка чата
    @commands.command(pass_context = True)
    @commands.has_permissions(view_audit_log = True)
    async def clear(self,ctx,amount = 1):
        await ctx.channel.purge(limit = amount + 1)
        print(f"[clear]:[{ctx.author}] очистил [{ctx.channel}] на {amount} строк")
# Повышение репутации
    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def rep_up(self,ctx,member: discord.Member = None):
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя для повышения репутации")
            print(f"[rep_up]:[{ctx.author}] не указал пользователя")
        elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] >= 15:
            await ctx.send(f"Невозможно повысить репутацию, так как она уже **максмимальна**")
            print(f"[rep_up]:Пользователь [{ctx.author}] хотел снизить репутацию [{member}], но она уже максимальна")
        else:
            await ctx.send(f"Репутация **повышена**")
            cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
            print(f"[rep_up]:Пользователь [{ctx.author}] повысил репутацию [{member}]")
            connection.commit()
# Снижение репутации
    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def rep_down(self,ctx,member: discord.Member = None):
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя для снижения репутации")
            print(f"[rep_down]:[{ctx.author}] не указал пользователя")
        elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] <= -5:
            await ctx.send(f"Невозможно снизить репутацию, так как она уже **минимальна**")
            print(f"[rep_down]:Пользователь [{ctx.author}] хотел снизить репутацию [{member}], но она уже минимальна")
        else:
            await ctx.send(f"Репутация **снижена**")
            cursor.execute("UPDATE users SET rep = rep - {} WHERE id = {}".format(1, member.id))
            print(f"[rep_down]:Пользователь [{ctx.author}] понизил репутацию [{member}]")
            connection.commit()
def setup(bot):
    print("moderator_commands.py ✅")
    bot.add_cog(moderator_commands(bot))