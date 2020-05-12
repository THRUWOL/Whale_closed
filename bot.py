import discord
import os
from discord.ext import commands
from discord.utils import get
import youtube_dl


bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('+')

# подключение к голосовому каналу
@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
# отключение от голосового канала
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
# удаление сообщений
@bot.command(pass_context=True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
# вывод текста
@bot.command(pass_context=True)
async def pzd(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('пизда')

@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удалён')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Жди...')

    voice = get(bot.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.voume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
