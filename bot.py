"""[МОДУЛИ И БИБЛИОТЕКИ]"""###############################################################################################################################################
import discord
import asyncio
import sqlite3
import os
from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag



"""[ВОСПОМОГАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ]"""#########################################################################################################################################
PREFIX = '.'
ID = # тут айди сообщения для выбора ролей по реакции
GUILD_ID = #ут айди канала
TOKEN = #тут токен

client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')
connection = sqlite3.connect('server.db')
cursor = connection.cursor()



"""[СОБЫТИЯ]"""##################################################################################################################################################################
# Действия при старте
@client.event
async def on_ready():
# Создание таблицы пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        rep REAL,
        lvl INT,
        exp INT
    )""")
    connection.commit()

# Создание таблицы магазина
    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")
    connection.commit()

    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 10, 1, 0)")
            else:
                pass
    connection.commit()

# Вывод сигнала работоспособности бота
    print("Кит поплыл")

# Вывод статуса бота
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = ".help"))

# Обновление таблицы
@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 10, 1, 0)")
        connection.commit()
    else:
        pass

# Опыт пользователя
@client.event
async def on_message(message):
    if len(message.content) > 10:
        for row in cursor.execute(f"SELECT exp, lvl, cash FROM users WHERE id = {message.author.id}"):
            expi = row[0]+10
            cursor.execute(f"UPDATE users SET exp = {expi} WHERE id = {message.author.id}")
            lvch = expi/(row[1]*100)
            lv = int(lvch)
            if row[1] < lv:
                await message.channel.send(f"**{message.author.name}** получает новый уровень")
                bal = 1000*lv
                cursor.execute(f"UPDATE users SET lvl={lv}, cash={bal} where id = {message.author.id}")
    await client.process_commands(message)
    connection.commit()

# Выдать роль по реакции
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'ratblanket':
            role = discord.utils.get(guild.roles, name='крыска')
        elif payload.emoji.name == 'gamer':
            role = discord.utils.get(guild.roles, name='геймер')
        elif payload.emoji.name == 'streamer':
            role = discord.utils.get(guild.roles, name='стример')
        elif payload.emoji.name == 'cyberclown':
            role = discord.utils.get(guild.roles, name='cyberclown')
        elif payload.emoji.name == 'music':
            role = discord.utils.get(guild.roles, name='музыкант')
        elif payload.emoji.name == 'art':
            role = discord.utils.get(guild.roles, name='художник')
        elif payload.emoji.name == 'prog':
            role = discord.utils.get(guild.roles, name='программист')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("Роль получена")
            else:
                print("Пользователь не найден")
        else:
            print("Роль не найдена")

# Убрать роль по реакции
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'ratblanket':
            role = discord.utils.get(guild.roles, name='крыска')
        elif payload.emoji.name == 'gamer':
            role = discord.utils.get(guild.roles, name='геймер')
        elif payload.emoji.name == 'streamer':
            role = discord.utils.get(guild.roles, name='стример')
        elif payload.emoji.name == 'cyberclown':
            role = discord.utils.get(guild.roles, name='cyberclown')
        elif payload.emoji.name == 'music':
            role = discord.utils.get(guild.roles, name='музыкант')
        elif payload.emoji.name == 'art':
            role = discord.utils.get(guild.roles, name='художник')
        elif payload.emoji.name == 'prog':
            role = discord.utils.get(guild.roles, name='программист')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("Роль убрана")
            else:
                print("Пользователь не найден")
        else:
            print("Роль не найдена")



"""[КОМАНДЫ]"""######################################################################################################################################################################33
# Очистка чата
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)

# Вывод баланса пользователя
@client.command()
async def balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :candy:**"""
        ))
    else:
        await ctx.send(embed = discord.Embed(
            description = f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :candy:**"""
        ))

# Вывод опыта пользователя
@client.command()
async def lvl(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            description = f"""Опыт пользователя **{ctx.author}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} единиц**. Уровень **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
        ))
    else:
        await ctx.send(embed = discord.Embed(
            description = f"""Опыт пользователя **{member}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} единиц**. Уровень **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
        ))

# Вывод репутации пользователя
@client.command()
async def rep(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            description = f"""Рейтинг пользователя **{ctx.author}** составляет **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} баллов**"""
        ))
    else:
        await ctx.send(embed = discord.Embed(
            description = f"""Рейтинг пользователя **{member}** составляет **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]} баллов**"""
        ))

# Снижение репутация
@client.command()
@commands.has_permissions(administrator = True)
async def rep_down(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя для снижения репутации")
    elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] <= -5:
        await ctx.send(f"Невозможно снизить репутацию, так как она уже **минимальна**")
    else:
        await ctx.send(f"Репутация **снижена**")
        cursor.execute("UPDATE users SET rep = rep - {} WHERE id = {}".format(0.1, member.id))
        connection.commit()

# Повышение репутации
@client.command()
@commands.has_permissions(administrator = True)
async def rep_up(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя для повышения репутации")
    elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] >= 15:
        await ctx.send(f"Невозможно повысить репутацию, так как она уже **максмимальна**")
    else:
        await ctx.send(f"Репутация **повышена**")
        cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(0.1, member.id))
        connection.commit()


# Дать конфеты пользователю
@client.command()
@commands.has_permissions(administrator = True)
async def award(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете выдать определённую сумму")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете начислить на счёт пользователя")
        elif amount < 1:
            await ctx.send(f"**{ctx.author}**, а вы очень щедры")
        else:
            await ctx.send(f"**{ctx.author}**, зачисление произошло успешно")
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
            connection.commit()

# Забрать конфеты у пользователя
@client.command()
@commands.has_permissions(administrator = True)
async def take(ctx, member: discord.Member = None, amount = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, у которого желаете отнять определённую сумму")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете отнять у пользователя")
        elif amount == 'all':
            await ctx.send(f"**{ctx.author}**, сбор дани произошёл успешно")
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connection.commit()
        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author}**, чёт не понял")
        else:
            await ctx.send(f"**{ctx.author}**, сбор дани произошёл успешно")
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()

# Добавление роли в магазин
@client.command()
@commands.has_permissions(administrator = True)
async def add_shop(ctx, role: discord.Role = None, cost: int = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую нужно внести в магазин")
    else:
        if cost is None:
            await ctx.send(f"**{ctx.author}**, укажите стоимость данной роли")
        elif cost < 0:
            await ctx.send(f"**{ctx.author}**, чёт не понял прикола")
        else:
            cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
            await ctx.send(f"Роль успешно добавлена")
            connection.commit()

# Удаление роли из магазина
@client.command()
@commands.has_permissions(administrator = True)
async def remove_shop(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую нужно удалить из магазина")
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        await ctx.send(f"Роль успешно убрана")
        connection.commit()

# Вывод магазина
@client.command()
async def shop(ctx):
    embed = discord.Embed(title = 'Магазин ролей', color = 0xffd700)
    for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
        if ctx.guild.get_role(row[0]) != None:
            embed.add_field(
                name = f"Стоимость {row[1]} :candy:",
                value = f"Вы приобретёте роль {ctx.guild.get_role(row[0]).mention}",
                inline = False
            )
        else:
            pass
    await ctx.send(embed = embed)

# Покупка в магазине
@client.command()
async def buy(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете купить")
    else:
        if role in ctx.author.roles:
            await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль")
        elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки")
        else:
            await ctx.author.add_roles(role)
            cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
            await ctx.send(f"Роль успешно куплена")
            connection.commit()

# Вывод команд
@client.command()
async def help(ctx):
    embed1 = discord.Embed(title = 'Команды пользователя', description = '.balance - узнать баланс конфет на своём счёту \n\n.balance @ник - узнать баланс другого пользователя \n\n.shop - открыть магазин \n\n.buy @роль - купить @роль в магазине\n\n')
    embed2 = discord.Embed(title = 'Команды администрации', description = '.clear N - очистка чата на N сообщений \n\n.award @ник N - дать пользователю N конфет \n\n.take @ник N - отнять у пользователя N конфет \n\n.take @ник all - отнять у пользователя все конфеты \n\n.add_shop @роль N - добавить в магазин @роль стоимостью N конфет \n\n.remove_shop @роль - убрать с магазина @роль \n\n')
    embeds = [embed1, embed2]
    message = await ctx.send(embed = embed1)
    page = pag(client, message, use_more=False, color = 0x7fc7ff, footer = False, embeds = embeds)
    await page.start()



"""[ЗАПУСК]"""###########################################################################################################################################################
# Запуск бота
client.run(TOKEN)
