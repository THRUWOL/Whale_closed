import discord
import asyncio
import sqlite3
import random
import os

import config

from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag

client = commands.Bot(command_prefix = config.PREFIX)
client.remove_command('help')
connection = sqlite3.connect('server.db')
cursor = connection.cursor()

# Действия при старте
@client.event
async def on_ready():
# Вывод статуса бота
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = ".help"))
    print("[bot_status]:Статус бота активен")

# Обновление таблицы
@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 10, 1, 0, 0, 0, 0)")
        connection.commit()
        print("[sql]:Таблица users была обновлена")
    else:
        pass

# Опыт пользователя
@client.event
async def on_message(message):
    if len(message.content) > 10:
        for row in cursor.execute(f"SELECT exp, lvl, cash FROM users WHERE id = {message.author.id}"):
            if cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0] == 15:
                expi = row[0]+20
            elif cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0] == -5:
                expi = row[0]+5
            elif cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0] == 228:
                expi = row[0]+0
            else:
                expi = row[0]+10
            cursor.execute(f"UPDATE users SET exp = {expi} WHERE id = {message.author.id}")
            lvch = expi/(row[1]*100)
            lv = int(lvch)
            if row[1] < lv:
                await message.channel.send(f"**{message.author.name}** получает новый уровень")
                bal = 1000*lv
                cursor.execute(f"UPDATE users SET lvl={lv}, cash= cash +{bal} where id = {message.author.id}")
                print(f"[lvl_up]:[{message.author.name}] получил уровень {lv}")
    await client.process_commands(message)
    connection.commit()

# Выдать роль по реакции
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == config.ID:
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
                print(f"[add_roles]:Пользователь [{member}] получает роль [{role.name}]")
            else:
                print("[add_roles]:Пользователь не найден")
        else:
            print(f"[add_roles]:Роль не найдена")

# Убрать роль по реакции
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == config.ID:
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
                print(f"[drop_roles]:Пользователь [{member}] снимает роль [{role.name}]") 
            else:
                print("[drop_roles]:Пользователь не найден")
        else:
            print("[drop_roles]:Роль не найдена")

# Очистка чата
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)
    print(f"[clear]:[{ctx.author}] очистил [{ctx.channel}] на {amount} строк")

# Вывод баланса пользователя
@client.command()
async def balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed( color = 0x3caa3c,
            description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :candy:**"""
        ))
        print(f"[balance]:Пользователь [{ctx.author}] вывел информацию о своём балансе")
    else:
        await ctx.send(embed = discord.Embed( color = 0x3caa3c,
            description = f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :candy:**"""
        ))
        print(f"[balance]:Пользователь [{ctx.author}] вывел информацию о балансе [{member}]")

# Вывод уровня пользователя
@client.command()
async def lvl(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed( color = 0xffa500,
            description = f"""Опыт пользователя **{ctx.author}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :star:**. Уровень **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
        ))
        print(f"[lvl]:Пользователь [{ctx.author}] вывел информацию о своём уровне")
    else:
        await ctx.send(embed = discord.Embed( color = 0xffa500,
            description = f"""Опыт пользователя **{member}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :star:**. Уровень **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**"""
        ))
        print(f"[lvl]:Пользователь [{ctx.author}] вывел информацию о уровне [{member}]")

# Вывод репутации пользователя
@client.command()
async def rep(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed( color = 0x9400d3,
            description = f"""Рейтинг пользователя **{ctx.author}** составляет **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :purple_heart:**"""
        ))
        print(f"[rep]:Пользователь [{ctx.author}] вывел информацию о своей репутации")
    else:
        await ctx.send(embed = discord.Embed( color = 0x9400d3,
            description = f"""Рейтинг пользователя **{member}** составляет **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :purple_heart:**"""
        ))
        print(f"[rep]:Пользователь [{ctx.author}] вывел информацию о репутации [{member}]")

# Вывод статистики по игре "камень, ножницы, бумага"
@client.command()
async def roll_stats(ctx, member: discord.Member = None):
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

# Снижение репутация
@client.command()
@commands.has_permissions(administrator = True)
async def rep_down(ctx, member: discord.Member = None):
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

# Повышение репутации
@client.command()
@commands.has_permissions(administrator = True)
async def rep_up(ctx, member: discord.Member = None):
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

# Дать конфеты пользователю
@client.command()
@commands.has_permissions(administrator = True)
async def award(ctx, member: discord.Member = None, amount: int = None):
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

# Забрать конфеты у пользователя
@client.command()
@commands.has_permissions(administrator = True)
async def take(ctx, member: discord.Member = None, amount = None):
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
@client.command()
@commands.has_permissions(administrator = True)
async def add_shop(ctx, role: discord.Role = None, cost: int = None):
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
@client.command()
@commands.has_permissions(administrator = True)
async def remove_shop(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую нужно удалить из магазина")
        print(f"[remove_shop]:[{ctx.author}] не указал роль для изъятия из магазина")
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        await ctx.send(f"Роль успешно убрана")
        print(f"[remove_shop]:[{ctx.author}] убрал из магазина роль [{role}]")
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
    print(f"[shop]:[{ctx.author}] вывел информацию о товарах в магазине")

# Покупка в магазине
@client.command()
async def buy(ctx, role: discord.Role = None):
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

# Отправка сообщений пользователям
@client.command(pass_context = True)
async def rps(message, member: discord.Member = None):
    emb = discord.Embed(title=f'Камень, ножницы, бумага',description='Выбирай, чем будешь сражаться.',colour=discord.Color.purple())

    message = await message.author.send(embed=emb)
    await message.add_reaction('🧻')
    await message.add_reaction('🗿')
    await message.add_reaction('✂️')
    
    print(message.author) 
    print(message.id)

# КаменьНожницыБумага (кинуть вызов)
@client.command()
async def roll_start(ctx, member: discord.Member = None, take = None, rps = ['камень', 'ножницы', 'бумагу']):    
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
@client.command()
async def rollend(ctx, member: discord.Member = None, take = None, rps = ['камень', 'ножницы', 'бумагу']):    
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

@client.command()
async def user_info(ctx, member: discord.Member = None):
    embed1 = discord.Embed(
        title = f'Информация о пользователе {member}',
        description = f'**Имя на сервере:** {member.display_name}\n **Репутация:** {cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :purple_heart:\n **Баланс:** {cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :candy:\n **Опыт:** {cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :star:\n **Уровень:** {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}\n **Высшая роль:** {member.top_role.mention}\n')   
    embed1.set_thumbnail(url = member.avatar_url)
    embed1.set_footer(text = f"Запросил {ctx.author}", icon_url=ctx.author.avatar_url)
    embed2 = discord.Embed(
        title = f'Ещё не придумал',
        description = f'Ждёмс')
    embeds = [embed1, embed2]
    message = await ctx.send(embed = embed1)
    page = pag(client, message, use_more = False, color = member.color, footer= False, embeds = embeds, timeout = 60)
    await page.start()

@client.command()
async def help(ctx):
    embed1 = discord.Embed(title = 'Команды пользователя', description = '.balance - узнать баланс конфет на своём счёту \n\n.balance @ник - узнать баланс другого пользователя \n\n.rep - узнать свою репутацию \n\n.rep @ник - узнать репутацию другого пользователя \n\n.lvl - получить информацию о своём уровне \n\n.lvl @ник - получить информацию о уровне другого пользователя \n\n.shop - открыть магазин \n\n.buy @роль - купить @роль в магазине\n\n')
    embed2 = discord.Embed(title = 'Игровые команды', description = 'КНБ - камень, ножницы, бумага \n\n.roll_start @имя - вызвать игрока на бой в КНБ \n\n.rollend @имя - принять вызов другого пользователя в КНБ \n\n.roll_stats - узнать свою статистику в КНБ \n\n.roll_stats - узнать статистику другого игрока в КНБ \n\n')
    embed3 = discord.Embed(title = 'Команды администрации', description = '.clear N - очистка чата на N сообщений \n\n.award @ник N - дать пользователю N конфет \n\n.take @ник N - отнять у пользователя N конфет \n\n.take @ник all - отнять у пользователя все конфеты \n\n.add_shop @роль N - добавить в магазин @роль стоимостью N конфет \n\n.remove_shop @роль - убрать с магазина @роль \n\n.rep_down @имя - снизить репутацию пользователя на 0.1 \n\n.rep_up @имя - повысить репутацию пользователя на 0.1')
    embeds = [embed1, embed2, embed3]
    message = await ctx.send(embed = embed1)
    page = pag(client, message, use_more=False, color = 0x7fc7ff, footer = False, embeds = embeds)
    print(f"[help]:[{ctx.author}] вывел информацию о командах сервера")
    await page.start()

# Запуск бота
print("~~~Кит поплыл~~~")
client.run(config.TOKEN)
