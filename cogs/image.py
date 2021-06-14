import discord
import requests
import time
import os
from discord.ext import commands
from functools import wraps
from PIL import Image as PILImage
from PIL import ImageOps, ImageDraw, ImageFont, ImageEnhance


times = os.path.join('..', 'resources', 'times.ttf')


def image(func):
    @wraps(func)
    async def image_inner(self, ctx, *args, **kwargs):
        if not ctx.message.attachments:
            await ctx.reply('You didn\'t attatch an image to edit!')
            return

        imageUrl = ctx.message.attachments[0].url.lower()
        if not imageUrl.lower().endswith(('png', 'jpg', 'webp', 'gif')):
            await ctx.reply('Inavlid image! It must be in PNG, JPG, WEBP, or GIF format')
            return

        r = requests.get(imageUrl, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/531.39.5 (KHTML, like Gecko) Version/5.0.2 Safari/531.39.5'})
        try:
            img = PILImage.open(r.raw)
        except:
            img = PILImage.open(r.content)

        filename = f'{time.time_ns()}.png'
        await func(img, filename, *args, **kwargs)

        imgfile = discord.File(filename, filename=filename)

        em = discord.Embed(
            title=f'{func.__name__.title()}-ed Image'
        )
        em.set_author(
            name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url=f'attachment://{filename}')

        await ctx.send(file=imgfile, embed=em)
        os.remove(filename)

    return image_inner


class Image(commands.Cog, description='Commands to create and edit images'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='WHAT? HOW?? | Parameters: text1, text2 (optional)\nMUST BE COMMA SEPARATED')
    @image
    async def what(img, filename, *text):
        text = ' '.join(text).split(',')
        text1 = text[0].strip()
        text2 = ','.join(text[1:]).strip()

        img = img.convert('RGB')
        img.thumbnail((400, 300), PILImage.ANTIALIAS)
        img = ImageOps.expand(img, border=20, fill='black')
        img = ImageOps.expand(img, border=2, fill='white')

        font = ImageFont.truetype(times, 90 if text2 == '' else 60)
        font2 = ImageFont.truetype(times, 40)

        imgW, imgH = img.size
        w = font.getsize(text1)[0]
        w2 = font2.getsize(text2)[0]

        out = PILImage.new("RGB", (800, 500))
        draw = ImageDraw.Draw(out)
        draw.text(((800-w)/2, 370), text1, 'white', font)
        draw.text(((800-w2)/2, 430), text2, 'white', font2)

        out.paste(img, ((800-imgW)//2, (380-imgH)//2))
        out.save(filename)

    @commands.command(help='👌👌😂😂😂 | Parameters: value (optional)')
    @image
    async def deepfry(img, filename, value: int = 10):
        value //= 5
        value = 10 if value > 10 else value
        value = 1 if value < 1 else value

        img = img.convert('RGB')
        img = ImageEnhance.Color(img).enhance(value)
        img = ImageEnhance.Sharpness(img).enhance(value*4)

        img.save(filename, quality=10-value)


def setup(bot):
    bot.add_cog(Image(bot))
