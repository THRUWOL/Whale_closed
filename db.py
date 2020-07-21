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

class db_events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
# Создание таблицы пользователей
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
#Создание таблицы config
        cursor.execute("""CREATE TABLE IF NOT EXISTS config (
            reaction_message_id BIGINT,
            rpg_ID BIGINT,
            rps_ID BIGINT
        )""")
        for guild in self.bot.guilds:
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
# Внесение данных нового пользователя при входе на сервер
    @commands.Cog.listener()
    async def on_member_join(self,member):
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
def setup(bot):
    print("db.py ✅")
    bot.add_cog(db_events(bot))