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

class rps_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# КаменьНожницыБумага (кинуть вызов)
    @commands.command()
    async def roll_start(self,ctx, member: discord.Member = None, take = None, rps = ['камень', 'ножницы', 'бумагу']):    
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя, с которым вы хотите играть")
        else:
            if cursor.execute(f"SELECT id_1 FROM rps WHERE id_1 = {ctx.author.id}").fetchone() is None or cursor.execute(f"SELECT id_2 FROM rps WHERE id_2 = {ctx.author.id}").fetchone() is None:
                if cursor.execute(f"SELECT id_1 FROM rps WHERE id_1 = {member.id}").fetchone() is None or cursor.execute(f"SELECT id_2 FROM rps WHERE id_2 = {member.id}").fetchone() is None:
                    if member.id == 709458389859565609 or member.id == 235088799074484224:
                        await ctx.send(f"Нельзя играть с ботом")
                    elif member.id == ctx.author.id:
                        await ctx.send(f"С самим собой? Лучше заведи друзей")
                    else: 
                        take = random.choice(rps)
                        await ctx.send(f"**{ctx.author}** вызывает на бой **{member}** и ставит **{take}**.")
                        await ctx.send(f"**{member}**, чтобы принять вызов введите команду **.rollend @имя**")
                        cursor.execute(f"INSERT INTO rps VALUES('{ctx.author}',{ctx.author.id}, '{member}', '{member.id}', 0, 0, 0)")
                        if take == 'камень':
                            cursor.execute(f"UPDATE rps SET start = 1 WHERE id_1 = {ctx.author.id}")
                        elif take == 'ножницы':
                            cursor.execute(f"UPDATE rps SET start = 2 WHERE id_1 = {ctx.author.id}")
                        else:
                            cursor.execute(f"UPDATE rps SET start = 3 WHERE id_1 = {ctx.author.id}")
                        connection.commit()
                else:
                    await ctx.send(f"У пользователя **{member}** есть незавершённая игра")
            else:
                await ctx.send(f"**{ctx.author}**, у вас осталась незавершённая игра")
# КаменьНожницыБумага (принять вызов)
    @commands.command()
    async def rollend(self,ctx, member: discord.Member = None, take = None, rps = ['камень', 'ножницы', 'бумагу']):    
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите имя соперника, который бросил вам вызов")
        elif cursor.execute(f"SELECT id_2 FROM rps WHERE id_1 = {member.id}").fetchone() is None: 
            await ctx.send(f"**{ctx.author}**, пользовател {member} не является вашим соперником")
        else:
            take = random.choice(rps)
            await ctx.send(f"**{ctx.author}** принимает вызов и ставит **{take}**.")
            if take == 'камень':
                cursor.execute(f"UPDATE rps SET end = 1 WHERE id_2 = {ctx.author.id}")
                if cursor.execute(f"SELECT start FROM rps WHERE id_2 = {ctx.author.id}").fetchone()[0] == 2:
                    await ctx.send(f"**{ctx.author}** победил")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET victories = victories + 1 WHERE id = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET defeats = defeats + 1 WHERE id = {member.id}")
                elif cursor.execute(f"SELECT start FROM rps WHERE id_2 = {ctx.author.id}").fetchone()[0] == 1:
                    await ctx.send(f"Ничья")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET draw = draw + 1 WHERE id = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET draw = draw + 1 WHERE id = {member.id}")
                else:
                    await ctx.send(f"**{member}** победил")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET victories = victories + 1 WHERE id = {member.id}")
                    cursor.execute(f"UPDATE users SET defeats = defeats + 1 WHERE id = {ctx.author.id}")
            elif take == 'ножницы':
                cursor.execute(f"UPDATE rps SET end = 2 WHERE id_2 = {ctx.author.id}")
                if cursor.execute(f"SELECT start FROM rps WHERE id_2 = {ctx.author.id}").fetchone()[0] == 3:
                    await ctx.send(f"**{ctx.author}** победил")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET victories = victories + 1 WHERE id = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET defeats = defeats + 1 WHERE id = {member.id}")
                elif cursor.execute(f"SELECT start FROM rps WHERE id_2 = {ctx.author.id}").fetchone()[0] == 2:
                    await ctx.send(f"Ничья")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET draw = draw + 1 WHERE id = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET draw = draw + 1 WHERE id = {member.id}")
                else:
                    await ctx.send(f"**{member}** победил")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET victories = victories + 1 WHERE id = {member.id}")
                    cursor.execute(f"UPDATE users SET defeats = defeats + 1 WHERE id = {ctx.author.id}")
            else:
                cursor.execute(f"UPDATE rps SET end = 3 WHERE id_2 = {ctx.author.id}")
                if cursor.execute(f"SELECT start FROM rps WHERE id_2 = {ctx.author.id}").fetchone()[0] == 1:
                    await ctx.send(f"**{ctx.author}** победил")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET victories = victories + 1 WHERE id = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET defeats = defeats + 1 WHERE id = {member.id}")
                elif cursor.execute(f"SELECT start FROM rps WHERE id_2 = {ctx.author.id}").fetchone()[0] == 3:
                    await ctx.send(f"Ничья")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET draw = draw + 1 WHERE id = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET draw = draw + 1 WHERE id = {member.id}")
                else:
                    await ctx.send(f"**{member}** победил")
                    cursor.execute(f"DELETE FROM rps WHERE id_2 = {ctx.author.id}")
                    cursor.execute(f"UPDATE users SET victories = victories + 1 WHERE id = {member.id}")
                    cursor.execute(f"UPDATE users SET defeats = defeats + 1 WHERE id = {ctx.author.id}")
            connection.commit()
# Вывод статистики по игре "камень, ножницы, бумага"
    @commands.command()
    async def roll_stats(self,ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed( color = 0xff4d00,
                description = f"""Игровая статистика **{ctx.author}**: Победы: **{cursor.execute("SELECT victories FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**, Поражения: **{cursor.execute("SELECT defeats FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**, Ничья: **{cursor.execute("SELECT draw FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
            ))
            print(f"[stats]:Пользователь [{ctx.author}] вывел свою игровую статистику")
        else:
            await ctx.send(embed = discord.Embed( color = 0xff4d00,
                description = f"""Игровая статистика **{member}**: Победы: **{cursor.execute("SELECT victories FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**, Поражения: **{cursor.execute("SELECT defeats FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**, Ничья: **{cursor.execute("SELECT draw FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**"""
            ))
            print(f"[stats]:Пользователь [{ctx.author}] вывел игровую статистику пользователя [{member}]")
def setup(bot):
    print("rps.py ✅")
    bot.add_cog(rps_commands(bot))