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

class helped(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Вывод анимированной задницы (команда администратора)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ass(self,ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'<a:butt_gala:729354694945669220>')
# Дать монетки пользователю (команда администратора)
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
# Забрать монетки у пользователя (команда администратора)
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
# Добавление роли в магазин (команда администратора)
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
# Удаление роли из магазина (команда администратора)
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
# Очистка чата (команда модератора)
    @commands.command(pass_context = True)
    @commands.has_permissions(view_audit_log = True)
    async def clear(self,ctx,amount = 1):
        await ctx.channel.purge(limit = amount + 1)
        print(f"[clear]:[{ctx.author}] очистил [{ctx.channel}] на {amount} строк")
# Повышение репутации (команда модератора)
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
# Снижение репутации (команда модератора)
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
    print("command.py ✅")
    bot.add_cog(helped(bot))