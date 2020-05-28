'''
Python bot for Discord
last update: 28 may 2020

by Nikita [thruwol] Yarosh
'''

import discord
import os
import asyncio
from discord.ext import commands

client = discord.Client(command_prefix = '.')

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
                print("done")
            else:
                print("Member not found")
        else:
            print("Role not found")

@client.command()
@commands.has_permissions(view_audit_log=True)
async def mute(ctx, member:discord.Member, time:int, reason):
    mute_role = discord.utils.get(ctx.guild.roles, id=715471240080654477)
    emb = discotd.Embed(title="Мут", color=0xff0000)
    emb.add_field(name='Модератор',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Нарушитель', value= member.mention,inline=False)
    emb.add_field(name='Причина', value=reason,inline=False)
    emb.add_field(name='Время',value=time,inline=False)
    await member.add_roles(mute_role)
    await.ctx.send(embed = emb)
    await asyncio.sleep(time*60)
    await member_remove_roles(mute_role)

# Запуск бота
client.run(os.environ.get('BOT_TOKEN'))
