"""
import discord
import os
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='.')

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
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import os
import requests
import discord
from discord.ext import commands
from discord.ext.commands import Bot

Bot = commands.Bot(command_prefix= '!')
client = discord.Client()

token = os.environ.get('BOT_TOKEN')

@Bot.event
async def on_ready():
    print("Bot is online")

headers = {'accept': '*/*',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'}

base_url = 'https://pikabu.ru/community/steam'


@Bot.command(pass_context = True)
async def free(ctx):
    #await ctx.message.delete()
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    soup = bs(request.content, 'lxml')
    title = soup.find('h2', attrs={'story__title'}).text
    href = soup.find('a', attrs={'story__title-link'})['href']
    content_text = soup.find('div', attrs = {'story-block story-block_type_text'}).text
    date = soup.find('time', attrs={'caption story__datetime hint'}).text
    await ctx.send(title)
    await ctx.send(content_text)
    await ctx.send(href)
    await ctx.send(date)

Bot.run(token)
