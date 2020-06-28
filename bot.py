'''
Python bot for Discord
last update: 28 june 2020

by Nikita [thruwol] Yarosh
'''

import discord
import os
import requests
import io
from PIL import Image, ImageFont, ImageDraw
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

@client.command(aliases = ['я', 'карта'])
async def card_user(ctx):
    img = Image.new('RGBA',(400, 200), '#232529')
    url = str(ctx.author.avatar_url)[:-10]

    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)

    img.paste(response, (15, 15, 115, 115))
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator

    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)

    idraw.text((145, 15), f'{name}#{tag}', font = headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

    img.save('user_card.png')

    await ctx.send(file = discord.File(fp = 'user_card.png'))


# Запуск бота
client.run(os.environ.get('BOT_TOKEN'))
