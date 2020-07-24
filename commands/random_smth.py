import discord
import asyncio
import sqlite3
import random
import os

from discord.ext import commands
from discord import Member, Guild
from Cybernator import Paginator as pag

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

wolf = [
    'https://memepedia.ru/wp-content/uploads/2019/04/memy-pro-volkov-3.jpg',
    'https://dm-st.ru/wp-content/uploads/2019/07/post_5d33994fa16cd.jpeg',
    'https://bmem.ru/wp-content/uploads/2019/11/sdelal-delo.jpg',
    'https://p4.tabor.ru/feed/2018-09-18/10289766/1132138_760x500.jpg',
    'https://bmem.ru/wp-content/uploads/2019/05/kazhdyy-dumaet-chto-znaet-menya-no-ne-kazhdyy-znaet-chto-ne-znaet-kto-dumaet.jpg',
    'https://i.pinimg.com/originals/55/e4/af/55e4afdb17f7e1f3949b3d9f652289a4.png',
    'https://i.pinimg.com/736x/17/62/84/176284f1b6cfbded8d06fa31d199fac9.jpg',
    'https://avatars.mds.yandex.net/get-pdb/2822660/3fa79715-f9cf-404e-9d47-deff126c523e/s1200?webp=false',
    'https://pbs.twimg.com/media/D7R3UKrXoAEpBk2.jpg:large',
    'https://dm-st.ru/wp-content/uploads/2019/07/post_5d33995037ee5.jpeg',
    'https://pbs.twimg.com/media/EDr72LbXoAAoGxC.jpg',
    'https://pbs.twimg.com/media/D-zvU2DXsAArCI2.jpg',
    'https://pbs.twimg.com/media/ENENM8PWsAQBZnC.jpg:large',
    'https://pbs.twimg.com/media/EbWBNnfXYAAdp3h.jpg',
    'https://i.pinimg.com/736x/1b/f6/f1/1bf6f1d7ec0ef1e9bd23f7f1c30b1fd3.jpg',
    'https://pbs.twimg.com/media/EFmjecqXkAAPAIo.jpg:large',
    'https://i.pinimg.com/originals/a1/1a/d6/a11ad6d798ca89169cd19bd20a2a6051.jpg',
    'https://sun9-3.userapi.com/c855020/v855020324/1c437c/Xnyf5aWZTY0.jpg',
    'https://pbs.twimg.com/media/EABei0SWwAAt68l.jpg:large',
    'https://pbs.twimg.com/media/D-99ap-W4AEicWn.jpg:large',
    'https://pbs.twimg.com/media/D7haEzCXkAAu2TF.jpg:large',
    'https://pbs.twimg.com/media/D6XeDt8V4AAwxZe.png:large',
    'https://sun9-32.userapi.com/c853620/v853620350/1d5d99/wSf9zua65KY.jpg',
    'https://sun9-7.userapi.com/c855428/v855428188/1d1a7c/48wQRgTtYPw.jpg',
    'https://pbs.twimg.com/media/EFIfyrtXUAAjQZX.jpg:large',
    'https://pbs.twimg.com/media/EC5nbj7XsAEk34i.jpg',
    'https://i.pinimg.com/originals/f3/19/40/f31940ee9fcab9f318241917126ac048.jpg',
    'https://pbs.twimg.com/media/EDo3im9XkAAB9t0.jpg',
    'https://pbs.twimg.com/media/D7_8RdnXUAAbubF.jpg',
    'https://pbs.twimg.com/media/EaC_zwWWoAExpz5.jpg',
    'https://pbs.twimg.com/media/D5ZNkkRXoAAqJfU.jpg:large',
    'https://sun3-11.userapi.com/nc8QXw5GBGYtiLZvhWLUBqumvYSjR9YEi3mvoA/APW6CvQWfsg.jpg',
    'https://i10.fotocdn.net/s118/d072707411534181/public_pin_m/2696361894.jpg',
    'https://prodota.ru/forum/uploads/monthly_2020_03/SQucwCWizaY.jpg.efdf9bc2792c0da5539841fa45098501.jpg',
    'https://sun9-41.userapi.com/c856524/v856524649/b9223/GuUZRFekY00.jpg',
    'https://pbs.twimg.com/media/EJYsWX1WkAAFqgu.jpg'
]

class random_smth(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
# Вывод цитат волка
    @commands.command()
    async def auf(self,ctx):
        chosen_image = random.choice(wolf)
        await ctx.send(chosen_image)

def setup(bot):
    print("random_smth.py ✅")
    bot.add_cog(random_smth(bot))