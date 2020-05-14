import discord
import os
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='.')

#test
client = discord.Client()
token = os.environ.get('BOT_TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)
