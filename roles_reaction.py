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

class role_events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Выдача роли по реакции
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        message_id = payload.message_id
        if message_id == config.ID:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
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
# Снятие роли по реакции
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        message_id = payload.message_id
        if message_id == config.ID:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
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
def setup(bot):
    print("roles_reaction.py ✅")
    bot.add_cog(role_events(bot))