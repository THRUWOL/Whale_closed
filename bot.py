'''
Python bot for Discord
last update: 15 may 2020

by Nikita [thruwol] Yarosh
'''
import config
import discord
import os
from discord import utils
from discord.ext import commands
from discord.utils import get

client = discord.Client()

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == '711626944608993340':
        print(payload.emoji.name)
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'poop':
            role = discord.utils.get(guild.roles, name = 'poop')

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("done")

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 'id':
        print(payload.emoji.name)

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("done")

@client.event
async def on_ready():
    print("Bot is ready!")

client.run(os.environ.get('BOT_TOKEN'))
