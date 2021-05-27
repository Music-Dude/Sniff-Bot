import discord
import requests
import time
import os
from discord.ext import commands
from PIL import Image, ImageOps, ImageDraw, ImageFont


class IMG(commands.Cog, description='Commands to create and edit images'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description='Create and modify images')
    async def image(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title='Invalid image command passed!',
                description='Use !help Image to view a list of commands',
                color=discord.Color.red()
            )
            await ctx.send(embed=em)

    @image.command(description='WHAT? HOW??')
    async def what(self, ctx, *text):
        if not ctx.message.attachments:
            await ctx.reply('You didn\'t attatch an image to edit!')
            return

        imageUrl = ctx.message.attachments[0].url.lower()
        if not imageUrl.endswith(('png', 'jpg', 'webp')):
            await ctx.reply('Inavlid image! It must be in the format PNG, JPG, or WEBP')
            return

        filename = str(int(time.time())) + '.jpg'
        text = ' '.join(text).split(', ')
        text1 = text[0]
        try:
            text2 = text[1]
        except:
            text2 = ''

        r = requests.get(imageUrl, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/531.39.5 (KHTML, like Gecko) Version/5.0.2 Safari/531.39.5'}).raw
        try:
            inputFile = Image.open(r.raw)
        except:
            inputFile = Image.open(r.content)

        inputFile.thumbnail((400, 300), Image.ANTIALIAS)
        inputFile = ImageOps.expand(inputFile, border=20, fill='black')
        inputFile = ImageOps.expand(inputFile, border=2, fill='white')

        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/times/times.ttf', 90 if text2 == '' else 60)
        font2 = ImageFont.truetype(
            '/usr/share/fonts/truetype/times/times.ttf', 40)

        imgW, imgH = inputFile.size
        w = font.getsize(text1)[0]
        w2 = font2.getsize(text2)[0]

        out = Image.new("RGB", (800, 500))
        draw = ImageDraw.Draw(out)
        draw.text(((800-w)/2, 370), text1, 'white', font)
        draw.text(((800-w2)/2, 430), text2, 'white', font2)

        out.paste(inputFile, ((800-imgW)//2, (380-imgH)//2))
        out.save(filename)

        await ctx.send(f'Requested by {ctx.author}', file=discord.File(filename))
        os.remove(filename)


def setup(bot):
    bot.add_cog(IMG(bot))
