'''
Python bot for Discord
last update: 28 may 2020

by Nikita [thruwol] Yarosh
'''

import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

# Проверка работоспособности
@client.event
async def on_ready():
    print("Bot is logged in")

# Выдать роль
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 715454105706823731:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, Bot.guilds)

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
                print("done")
            else:
                print("Member not found")
        else:
            print("Role not found")

# Убрать роль
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 715454105706823731:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, Bot.guilds)

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
                print("done")
            else:
                print("Member not found")
        else:
            print("Role not found")

# Выдать мут
@client.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

    await member.add_roles(mute_role)
    await ctx.send(f'У {member.mention}, ограничение чата за нарушение прав!')

# Убрать мут
@client.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

    await member.remove_roles(mute_role)


# Запуск бота
client.run(os.environ.get('BOT_TOKEN'))
