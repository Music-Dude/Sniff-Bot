import discord
import requests
import textwrap
import time
import os
from colors import colordict
from urllib.parse import quote
from discord.ext import commands
from functools import wraps
from PIL import Image as PILImage
from PIL import ImageOps, ImageDraw, ImageFont, ImageEnhance


times = os.path.join('..', 'resources', 'times')
impact = os.path.join('..', 'resources', 'impact')


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
            title=f'{func.__name__.title()}ed Image'
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

    @commands.command(help='Render text as a PNG image', pass_context=True)
    async def text(self, ctx, *, args='Your text here, ffffff'):
        try:
            args = args.split(',')
            for x, arg in enumerate(args):
                args[x] = arg.strip()
            text = args[0]

        except:
            await ctx.send('Couldn\'t get an image for that. Make sure everything is formatted like this:\n`!text Your text here, color`')
            return
        try:
            color = colordict[args[1].lower()]
        except:
            color = 'ffffff'

        em = discord.Embed(
            title='Generated text',
            color=int(hex(int(color, 16)), 0)
        )
        em.set_author(
            name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        url = f'https://lingtalfi.com/services/pngtext?text=%20{quote(text)}%20&color={color}&size=100'
        em.set_image(url=url)
        await ctx.send(embed=em)

    @commands.command(help='Caption an image')
    @image
    async def caption(img, filename, *text):
        text = ' '.join(text).split(',')
        text1 = text[0].strip()
        text2 = ','.join(text[1:]).strip()

        img = img.convert('RGB')
        imgW, imgH = img.size

        fontsize = imgH//12
        font = ImageFont.truetype(impact, fontsize)

        charW, charH = font.getsize('A')
        charsPerLine = imgW//charW*1.5
        top = textwrap.wrap(text1, width=charsPerLine, break_long_words=False)
        bottom = textwrap.wrap(text2, width=charsPerLine,
                               break_long_words=False)

        draw = ImageDraw.Draw(img)

        y = 10
        for line in top:
            line_width, line_height = font.getsize(line)
            x = (imgW - line_width)/2
            draw.text((x, y), line, fill='white', font=font)
            y += line_height

        y = imgH - charH * len(bottom) - 15
        for line in bottom:
            line_width, line_height = font.getsize(line)
            x = (imgW - line_width)/2
            draw.text((x, y), line, fill='white', font=font)
            y += line_height

        img.save(filename)

    @commands.command(help='WHAT? HOW??')
    @image
    async def what(img, filename, *text):
        text = ' '.join(text).split(',')
        text1 = text[0].strip()
        text2 = ','.join(text[1:]).strip()

        img = img.convert('RGB')
        img.thumbnail((700, 320), PILImage.ANTIALIAS)
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

    @commands.command(help='👌👌😂😂😂')
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
