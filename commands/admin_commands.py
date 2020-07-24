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

class admin_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Вывод анимированной задницы
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ass(self,ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'<a:butt_gala:729354694945669220>')
# Дать монетки пользователю
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def award(self,ctx,member: discord.Member = None,amount: int = None):
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете выдать определённую сумму")
            print(f"[award]:[{ctx.author}] не указал пользователя")
        else:
            if amount is None:
                await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете начислить на счёт пользователя")
                print(f"[award]:[{ctx.author}] не указал сумму начисления для [{member}]")
            elif amount < 1:
                await ctx.send(f"**{ctx.author}**, а вы очень щедры")
                print(f"[award]:[{ctx.author}] указал сумму начисления для [{member}], но она < 1")
            else:
                await ctx.send(f"**{ctx.author}**, зачисление произошло успешно")
                print(f"[award]:[{ctx.author}] выдал [{member}] {amount} конфет")
                cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
                connection.commit()
# Забрать монетки у пользователя
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def take(self,ctx,member: discord.Member = None,amount = None):
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя, у которого желаете отнять определённую сумму")
            print(f"[take]:[{ctx.author}] не указал пользователя")
        else:
            if amount is None:
                await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете отнять у пользователя")
                print(f"[take]:[{ctx.author}] не указал сумму взимания для [{member}]")
            elif amount == 'all':
                await ctx.send(f"**{ctx.author}**, сбор дани произошёл успешно")
                cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
                print(f"[take]:[{ctx.author}] изъял все конфеты у [{member}]")
                connection.commit()
            elif int(amount) < 1:
                await ctx.send(f"**{ctx.author}**, чёт не понял")
                print(f"[take]:[{ctx.author}] указал сумму взимания для [{member}], но она < 1")
            else:
                await ctx.send(f"**{ctx.author}**, сбор дани произошёл успешно")
                cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
                print(f"[take]:[{ctx.author}] изъял у [{member}] {amount} конфет")
                connection.commit()
# Добавление роли в магазин
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def shop_add(self,ctx,role: discord.Role = None,cost: int = None):
        if role is None:
            await ctx.send(f"**{ctx.author}**, укажите роль, которую нужно внести в магазин")
            print(f"[add_shop]:[{ctx.author}] не указал роль для добавления в магазин")
        else:
            if cost is None:
                await ctx.send(f"**{ctx.author}**, укажите стоимость данной роли")
                print(f"[add_shop]:[{ctx.author}] не указал стоимость для [{role}]")
            elif cost < 0:
                await ctx.send(f"**{ctx.author}**, чёт не понял прикола")
                print(f"[add_shop]:[{ctx.author}] указал стоимость для [{role}], но она < 0")
            else:
                cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
                await ctx.send(f"Роль успешно добавлена")
                print(f"[add_shop]:[{ctx.author}] пустил в продажу роль [{role}] за {cost} конфет")
                connection.commit()
# Удаление роли из магазина 
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def shop_remove(self,ctx,role: discord.Role = None):
        if role is None:
            await ctx.send(f"**{ctx.author}**, укажите роль, которую нужно удалить из магазина")
            print(f"[remove_shop]:[{ctx.author}] не указал роль для изъятия из магазина")
        else:
            cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
            await ctx.send(f"Роль успешно убрана")
            print(f"[remove_shop]:[{ctx.author}] убрал из магазина роль [{role}]")
            connection.commit()
def setup(bot):
    print("admin_commands.py ✅")
    bot.add_cog(admin_commands(bot))