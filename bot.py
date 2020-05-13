import discord
import os
from discord.ext import commands
from discord.utils import get
import youtube_dl


bot = commands.Bot(command_prefix='#')

@bot.event
async def on_ready():
    print('+')


@bot.command(pass_context=True)
async def bot(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('буль')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
