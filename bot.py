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

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        rep REAL,
        lvl INT,
        exp INT,
        victories INT,
        defeats INT,
        draw INT,
        server_id INT
    )""")
    connection.commit()

# Создание таблицы магазина
    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")
    connection.commit()

# Создание таблицы rps
    cursor.execute("""CREATE TABLE IF NOT EXISTS rps (
        player1 TEXT,
        id_1 INT,
        player2 TEXT,
        id_2 INT,
        start INT,
        end INT,
        result INT
    )""")
    connection.commit()

# Создание таблицы rpg_monster
    cursor.execute("""CREATE TABLE IF NOT EXISTS rpg_monster (
        monster_name CHAR,
        monster_damage INT,
        monster_health INT
    )""")
    connection.commit()

#Создание таблицы rpg_users
    cursor.execute("""CREATE TABLE IF NOT EXISTS rpg_users (
        name TEXT,
        id INT,
        coin INT,
        damage INT,
        healt INT,
        armor INT
    )""")
    connection.commit()

#Создание таблицы rpg_battle
    cursor.execute("""CREATE TABLE IF NOT EXISTS rpg_battle (
        name TEXT,
        id INT,
        monster_name TEXT,
        monster_health INT,
        monster_damage INT,
        user_damage INT
    )""")
    connection.commit()

    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM rpg_users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO rpg_users VALUES('{member}', {member.id}, 0, 5, 100, 0)")
            else:
                pass

            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 10, 1, 0, 0, 0, 0, {guild.id})")
            else:
                pass
    connection.commit()

# Вывод статуса бота
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = ".help"))
    print("[bot_status]:Статус бота активен")

# Обновление таблицы
@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM rpg_users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO rpg_users VALUES('{member}', {member.id}, 0, 5, 100, 0)")
        print("[sql]:Таблица rpg_users была обновлена")
    else:
        pass

    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 10, 1, 0, 0, 0, 0, {member.guild.id})")
        print("[sql]:Таблица users была обновлена")
    else:
        pass
    connection.commit()

# Опыт пользователя
@client.event
async def on_message(message):
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
    await client.process_commands(message)
    connection.commit()
    print(f' *** [{message.channel}]:[{message.author.display_name}]: {message.content}')

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
async def rpg_battle(ctx, random_monster = [1], monster = None):
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


# Вывод всех команд сервера
@client.command()
async def help(ctx):
    embed1 = discord.Embed(title = 'Команды пользователя', description = '.balance - узнать баланс конфет на своём счёту \n\n.balance @ник - узнать баланс другого пользователя \n\n.rep - узнать свою репутацию \n\n.rep @ник - узнать репутацию другого пользователя \n\n.lvl - получить информацию о своём уровне \n\n.lvl @ник - получить информацию о уровне другого пользователя \n\n.shop - открыть магазин \n\n.buy @роль - купить @роль в магазине\n\n .leaderboard - вывод рейтинговой таблицы \n\n .user_info @ник - вывод полной статистики пользователя')
    embed2 = discord.Embed(title = 'Игровые команды', description = 'КНБ - камень, ножницы, бумага \n\n.roll_start @имя - вызвать игрока на бой в КНБ \n\n.rollend @имя - принять вызов другого пользователя в КНБ \n\n.roll_stats - узнать свою статистику в КНБ \n\n.roll_stats - узнать статистику другого игрока в КНБ \n\n .rpg_battle - начать бой с монстром \n\n .atack - атаковать монстра \n\n')
    embed4 = discord.Embed(title = 'Команды администратора', description = '.award @ник N - дать пользователю N конфет \n\n.take @ник N - отнять у пользователя N конфет \n\n.take @ник all - отнять у пользователя все конфеты \n\n.shop_add @роль N - добавить в магазин @роль стоимостью N конфет \n\n.shop_remove @роль - убрать с магазина @роль \n\n')
    embed3 = discord.Embed(title = 'Команды помощника', description ='.clear N - очистка чата на N сообщений \n\n .rep_down @имя - снизить репутацию пользователя на 1 \n\n.rep_up @имя - повысить репутацию пользователя на 1')
    embeds = [embed1, embed2, embed3, embed4]
    message = await ctx.send(embed = embed1)
    page = pag(client, message, use_more=False, color = 0x7fc7ff, footer = False, embeds = embeds)
    print(f"[help]:[{ctx.author}] вывел информацию о командах сервера")
    await page.start()
# Вывод информации о пользователе
@client.command()
async def user_info(ctx,member: discord.Member = None):
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
    page = pag(client, message, use_more = False, color = member.color, footer= False, embeds = embeds, timeout = 60)
    await page.start()
# Вывод доски почёта (5 пользователей)
@client.command()
async def leaderboard(ctx):
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
    page = pag(client, message, use_more = False, color = 0xff4d00, footer = False, embeds = embeds, timeout = 60)
    await page.start()

@client.command()
async def atack(ctx):
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


extensions = ['command']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

print("~~~Кит поплыл~~~")
client.run(config.TOKEN)