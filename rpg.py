import discord
import asyncio
import sqlite3
import random
import os

import config

from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class rpg_play(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Вызов монстра на бой
    @commands.command()
    async def rpg_battle(self,ctx, random_monster = [1], monster = None):
        if cursor.execute(f"SELECT id FROM rpg_battle WHERE id = {ctx.author.id}").fetchone() is None:
            monster = random.choice(random_monster)
            if cursor.execute(f"SELECT monster_name FROM rpg_monster WHERE rowid = {monster}"):
                embed = discord.Embed(title = 'Нападение монстра')
                embed.add_field(
                    name = f'Происхождение: {cursor.execute("SELECT monster_name FROM rpg_monster WHERE rowid = {}".format(monster)).fetchone()[0]}',
                    value = f'Здоровье: {cursor.execute("SELECT monster_health FROM rpg_monster WHERE rowid = {}".format(monster)).fetchone()[0]} \n Сила атаки: {cursor.execute("SELECT monster_damage FROM rpg_monster WHERE rowid = {}".format(monster)).fetchone()[0]}',
                    inline = False
                )
                embed.add_field(
                    name = f'Герой: {ctx.author.display_name}',
                    value = f'Здоровье: {cursor.execute("SELECT health FROM rpg_users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} \n Сила атаки: {cursor.execute("SELECT damage FROM rpg_users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} \n Броня: {cursor.execute("SELECT armor FROM rpg_users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}',
                    inline = False
                )
                embed.set_footer(text = f'С монстром сражается {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url = config.zombie)
            await ctx.send(embed=embed)
            cursor.execute("INSERT INTO rpg_battle VALUES('{}', {}, {}, {}, {}, {})".format(ctx.author, ctx.author.id, cursor.execute("SELECT rowid FROM rpg_monster WHERE rowid = {}".format(monster)).fetchone()[0], cursor.execute("SELECT monster_health FROM rpg_monster WHERE rowid = {}".format(monster)).fetchone()[0], cursor.execute("SELECT monster_damage FROM rpg_monster WHERE rowid = {}".format(monster)).fetchone()[0], cursor.execute("SELECT damage FROM rpg_users WHERE id = {}".format(ctx.author.id)).fetchone()[0]))
        else:
            await ctx.send(f"Сначала разберись с прошлым противником")
        connection.commit()
# Ударить монстра
    @commands.command()
    async def atack(self,ctx):
        await ctx.channel.purge(limit = 1)
        if cursor.execute(f"SELECT id FROM rpg_battle WHERE id = {ctx.author.id}").fetchone() is None:
            await ctx.send(f"{ctx.author.display_name} ударил(а) палкой по крапиве")
        else:
            if cursor.execute(f"SELECT monster_health FROM rpg_battle WHERE id = {ctx.author.id}").fetchone()[0] > 0:
                cursor.execute(f"UPDATE rpg_battle SET monster_health = monster_health - user_damage WHERE id = {ctx.author.id}")
                cursor.execute(f"""UPDATE rpg_users SET health = health - {cursor.execute("SELECT monster_damage FROM rpg_battle WHERE id = {}".format(ctx.author.id)).fetchone()[0]} WHERE id = {ctx.author.id}""")
                connection.commit()
                await ctx.channel.purge(limit = 1)
                embed = discord.Embed(title = 'Битва')
                embed.add_field(
                    name = f'Происхождение: {cursor.execute("SELECT monster_name FROM rpg_monster WHERE rowid ={}".format(cursor.execute("SELECT monster_id FROM rpg_battle WHERE id = {}".format(ctx.author.id)).fetchone()[0])).fetchone()[0]}',
                    value = f'Здоровье: {cursor.execute("SELECT monster_health FROM rpg_battle WHERE id = {}".format(ctx.author.id)).fetchone()[0]} \n Сила атаки: {cursor.execute("SELECT monster_damage FROM rpg_battle WHERE id = {}".format(ctx.author.id)).fetchone()[0]}',
                    inline = False
                )
                embed.add_field(
                    name = f'Герой: {ctx.author.display_name}',
                    value = f'Здоровье: {cursor.execute("SELECT health FROM rpg_users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} \n Сила атаки: {cursor.execute("SELECT user_damage FROM rpg_battle WHERE id = {}".format(ctx.author.id)).fetchone()[0]}',
                    inline = False
                )
                embed.set_footer(text = f'В сражении учавствует {ctx.author.display_name}', icon_url = ctx.author.avatar_url)
                embed.set_thumbnail(url = config.zombie)
                await ctx.send(embed = embed)
            else:
                await ctx.send(f"Монстр убит")
                cursor.execute(f"DELETE FROM rpg_battle WHERE id = {ctx.author.id}")
        connection.commit()
def setup(bot):
    print("rpg.py ✅")
    bot.add_cog(rpg_play(bot))