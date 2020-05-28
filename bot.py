'''
Python bot for Discord
last update: 15 may 2020

by Nikita [thruwol] Yarosh
'''

import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is logged in")

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 711626944608993340:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, cient.guilds)

        if payload.emoji.name == 'cpp':
            print("C++ Role")
            role = discord.utils.get(guild.roles, name='C++')
        elif payload.emoji.name == 'clang':
            print("C Role")
            role = discord.utils.get(guild.roles, name='C')
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

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 711626944608993340:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, cient.guilds)

        if payload.emoji.name == 'cpp':
            print("C++ Role")
            role = discord.utils.get(guild.roles, name='C++')
        elif payload.emoji.name == 'clang':
            print("C Role")
            role = discord.utils.get(guild.roles, name='C')
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

bot.run(os.environ.get('BOT_TOKEN'))
