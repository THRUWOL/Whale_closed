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

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = ".help"))
    print("[bot_status]:Статус бота активен")

# опыт
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
'''
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
'''
extensions = ['command','roles_reaction','db','rps','rpg']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

print("~~~Кит поплыл~~~")
client.run(config.TOKEN)