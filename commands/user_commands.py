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

class user_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Вывод баланса пользователя
    @commands.command()
    async def balance(self,ctx,member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed( color = 0x3caa3c,
                description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} <a:Coin:733734700098781205>**"""
            ))
            print(f"[balance]:Пользователь [{ctx.author}] вывел информацию о своём балансе")
        else:
            await ctx.send(embed = discord.Embed( color = 0x3caa3c,
                description = f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} <a:Coin:733734700098781205>**"""
            ))
            print(f"[balance]:Пользователь [{ctx.author}] вывел информацию о балансе [{member}]")
# Вывод уровня и опыта пользователя
    @commands.command()
    async def lvl(self,ctx,member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed( color = 0xffa500,
                description = f"""Опыт пользователя **{ctx.author}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} <a:star_red:733736417523531798>**. Уровень **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
            ))
            print(f"[lvl]:Пользователь [{ctx.author}] вывел информацию о своём уровне")
        else:
            await ctx.send(embed = discord.Embed( color = 0xffa500,
                description = f"""Опыт пользователя **{member}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} <a:star_red:733736417523531798>**. Уровень **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**"""
            ))
            print(f"[lvl]:Пользователь [{ctx.author}] вывел информацию о уровне [{member}]")
# Вывод репутации пользователя
    @commands.command()
    async def rep(self,ctx,member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed( color = 0x9400d3,
                description = f"""Рейтинг пользователя **{ctx.author}** составляет **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} <a:Rainbow_Heart:733734474725982338>**"""
            ))
            print(f"[rep]:Пользователь [{ctx.author}] вывел информацию о своей репутации")
        else:
            await ctx.send(embed = discord.Embed( color = 0x9400d3,
                description = f"""Рейтинг пользователя **{member}** составляет **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]} <a:Rainbow_Heart:733734474725982338>**"""
            ))
            print(f"[rep]:Пользователь [{ctx.author}] вывел информацию о репутации [{member}]")
# Покупка ролей в магазине
    @commands.command()
    async def buy(self,ctx,role: discord.Role = None):
        if role is None:
            await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете купить")
            print(f"[buy]:[{ctx.author}] не указал роль, которую желает купить")
        else:
            if role in ctx.author.roles:
                await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль")
                print(f"[buy]:[{ctx.author}] уже имеет роль [{role}]")
            elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
                await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки")
                print(f"[buy]: У пользователя [{ctx.author}] недостаточно средств для покупки роли [{role}]")
            else:
                await ctx.author.add_roles(role)
                cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
                await ctx.send(f"Роль успешно куплена")
                print(f"[buy]:[{ctx.author}] приобрёл роль [{role}]")
                connection.commit()
# Вывод магазина
    @commands.command()
    async def shop(self,ctx):
        embed = discord.Embed(title = 'Магазин ролей', color = 0xffd700)
        for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
            if ctx.guild.get_role(row[0]) != None:
                embed.add_field(
                    name = f"Стоимость {row[1]} <a:Coin:733734700098781205>",
                    value = f"Вы приобретёте роль {ctx.guild.get_role(row[0]).mention}",
                    inline = False
                )
            else:
                pass
        await ctx.send(embed = embed)
        print(f"[shop]:[{ctx.author}] вывел информацию о товарах в магазине")
# Вывод команд сервера
    @commands.command()
    async def help(self,ctx):
        embed1 = discord.Embed(title = 'Команды пользователя', description = '.balance - узнать баланс конфет на своём счёту \n\n.balance @ник - узнать баланс другого пользователя \n\n.rep - узнать свою репутацию \n\n.rep @ник - узнать репутацию другого пользователя \n\n.lvl - получить информацию о своём уровне \n\n.lvl @ник - получить информацию о уровне другого пользователя \n\n.shop - открыть магазин \n\n.buy @роль - купить @роль в магазине\n\n .leaderboard - вывод рейтинговой таблицы \n\n .user_info @ник - вывод полной статистики пользователя')
        embed2 = discord.Embed(title = 'Игровые команды', description = 'КНБ - камень, ножницы, бумага \n\n.roll_start @имя - вызвать игрока на бой в КНБ \n\n.rollend @имя - принять вызов другого пользователя в КНБ \n\n.roll_stats - узнать свою статистику в КНБ \n\n.roll_stats - узнать статистику другого игрока в КНБ \n\n .rpg_battle - начать бой с монстром \n\n .atack - атаковать монстра \n\n')
        embed4 = discord.Embed(title = 'Команды администратора', description = '.award @ник N - дать пользователю N конфет \n\n.take @ник N - отнять у пользователя N конфет \n\n.take @ник all - отнять у пользователя все конфеты \n\n.shop_add @роль N - добавить в магазин @роль стоимостью N конфет \n\n.shop_remove @роль - убрать с магазина @роль \n\n')
        embed3 = discord.Embed(title = 'Команды помощника', description ='.clear N - очистка чата на N сообщений \n\n .rep_down @имя - снизить репутацию пользователя на 1 \n\n.rep_up @имя - повысить репутацию пользователя на 1')
        embeds = [embed1, embed2, embed3, embed4]
        message = await ctx.send(embed = embed1)
        page = pag(self.bot, message, use_more=False, color = 0x7fc7ff, footer = False, embeds = embeds)
        print(f"[help]:[{ctx.author}] вывел информацию о командах сервера")
        await page.start()
# Вывод информации о пользователе
    @commands.command()
    async def user_info(self,ctx,member: discord.Member = None):
        embed1 = discord.Embed(
            title = f'Информация о пользователе',
            description = f'**Ник в дискорде:** {member}\n**Ник на сервере:** {member.display_name}\n **Репутация:** {cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]} <a:Rainbow_Heart:733734474725982338>\n **Баланс:** {cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} <a:Coin:733734700098781205>\n **Опыт:** {cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} <a:star_red:733736417523531798>\n **Уровень:** {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}\n **Высшая роль:** {member.top_role.mention}\n')   
        embed1.set_thumbnail(url = member.avatar_url)
        embed1.set_footer(text = f"Запрос от пользователя {ctx.author}", icon_url=ctx.author.avatar_url)
        embed2 = discord.Embed(
            title = f'Статистика в КНБ',
            description = f'**Победы:** {cursor.execute("SELECT victories FROM users WHERE id = {}".format(member.id)).fetchone()[0]}\n **Поражения:** {cursor.execute("SELECT defeats FROM users WHERE id = {}".format(member.id)).fetchone()[0]}\n **Ничья:** {cursor.execute("SELECT draw FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')
        embed2.set_thumbnail(url = member.avatar_url)
        embed2.set_footer(text = f"Запрос от пользователя {ctx.author}", icon_url=ctx.author.avatar_url)
        embed3 = discord.Embed(
            title = f'Достижения[beta]',
            description = f'Скоро появятся...'
        )
        embeds = [embed1, embed2, embed3]
        message = await ctx.send(embed = embed1)
        page = pag(self.bot, message, use_more = False, color = member.color, footer= False, embeds = embeds, timeout = 60)
        await page.start()
# Вывод доски почёта (5 пользователей)
    @commands.command()
    async def leaderboard(self,ctx):
        embed1 = discord.Embed(title = 'Богачи сервера')
        counter = 0
        for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 5".format(ctx.guild.id)):
            counter += 1
            embed1.add_field(
                name = f'{counter} | {row[0]}',
                value = f'Баланс: {row[1]} <a:Coin:733734700098781205>',
                inline = False
            )
        embed2 = discord.Embed(title = 'Качки сервера')
        counter = 0
        for row in cursor.execute("SELECT name, exp, lvl FROM users WHERE server_id = {} ORDER BY exp DESC LIMIT 5".format(ctx.guild.id)):
            counter += 1
            embed2.add_field(
                name = f'{counter} | {row[0]}',
                value = f'Уровень: {row[2]} | Опыт: {row[1]} <a:star_red:733736417523531798>',
                inline = False
            )
        embed3 = discord.Embed(title = 'Порядочное общество')
        counter = 0
        for row in cursor.execute("SELECT name, rep FROM users WHERE server_id = {} ORDER BY rep DESC LIMIT 5".format(ctx.guild.id)):
            counter += 1
            embed3.add_field(
                name = f'{counter} | {row[0]}',
                value = f'Репутация: {row[1]} <a:Rainbow_Heart:733734474725982338>',
                inline = False
            )
        embeds = [embed1, embed2, embed3]
        message = await ctx.send(embed = embed1)
        page = pag(self.bot, message, use_more = False, color = 0xff4d00, footer = False, embeds = embeds, timeout = 60)
        await page.start()
# Вывод аватарки пользователя
    @commands.command()
    async def avatar(self,ctx,member: discord.Member):
        await ctx.send('{}'.format(member.avatar_url))
def setup(bot):
    print("user_commands.py ✅")
    bot.add_cog(user_commands(bot))