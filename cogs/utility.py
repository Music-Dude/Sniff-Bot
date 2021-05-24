import discord
import requests
import random
import asyncio
import config
from string import ascii_letters, digits
from colors import colordict
from urllib.parse import quote
from discord.ext import commands


class Utility(commands.Cog, description='Somewhat useful commands'):
    def __init__(self, bot):
        self.bot = bot

    def check_author(self, author):
        def inner_check(message):
            return message.author == author
        return inner_check

    @commands.command(help='Times your typing of words')
    async def verify(self, ctx):
        verified_role = ctx.guild.get_role(config.verified_role)

        if verified_role in ctx.author.roles:
            await ctx.author.send(f'You are already verified in {ctx.guild}!')
            return

        if ctx.guild == None:
            await ctx.reply('This command can only be used in a server!')
            return

        try:
            await ctx.message.delete()
        except:
            pass

        col = discord.Color.random()

        em = discord.Embed(
            title=f'Verification for {ctx.guild}',
            description='We need to make sure you\'re human',
            color=col
        
        )
        captcha = ''.join(random.choices(ascii_letters + digits, k=5))
        em.set_image(url=f'https://lingtalfi.com/services/pngtext?text=%20{captcha}%20&color={str(col)[1:]}&size=100')

        verifyMessage = await ctx.author.send(embed=em)
        
        try:
            answer = await self.bot.wait_for('message', check=self.check_author(ctx.author), timeout=30)
        except asyncio.TimeoutError:
            await verifyMessage.edit(content='Sorry, you took too long to reply.', embed=None)
            return

        em = discord.Embed(
            title = f'Successfully verified in {ctx.guild}!',
            description='Have fun!',
            color=col
        )

        if captcha in answer.content:
            await verifyMessage.edit(embed=em)
            try:
                await ctx.author.add_roles(verified_role)
            except:
                await answer.channel.send('Sorry, failed to give you the verified role. Please contact a staff member if the issue persists.')
        else:
            await answer.reply('Failed to verify! Try again.')

    @commands.command(help="Show current member count", aliases=["membercount"])
    async def members(self, ctx):
        em = discord.Embed(
        title=f"Members in {ctx.guild}",
        description=f"```{ctx.guild.member_count}```",
        color=discord.Color.blurple()
        )

        await ctx.send(embed=em)

    @commands.command(help='Gets bot latency', aliases=['latency'])
    async def ping(self, ctx):
        em = discord.Embed(
            title='Pinging. . .',
            description=f'{round(self.bot.latency, 3)}ms',
            color=discord.Color.gold()
        )
        await ctx.send(embed=em)

    @commands.command(help='Gets a user\'s profile picture', aliases=['avatar'])
    async def pfp(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        em = discord.Embed(
            title=f'{user}\'s avatar'
        )
        em.set_footer(text=f'Requested by {ctx.author}')
        em.set_image(url=user.avatar_url)
        await ctx.send(embed=em)

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

    @commands.command(help='Gets the current BTC price', aliases=['bitcoin'])
    async def btc(self, ctx):
        r = requests.get(
            'https://api.coindesk.com/v1/bpi/currentprice/USD.json').json()
        price = r['bpi']['USD']['rate']
        em = discord.Embed(title='BTC Price', color=0xD9B166)
        em.set_author(
            name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.add_field(name='USD', value=f'${price}')
        em.set_footer(text=r['disclaimer'])
        em.set_thumbnail(
            url='https://static.currency.com/img/media/bitcoin.dd8a16.png')
        await ctx.send(embed=em)

    @commands.command(help='Make a suggestion for Sniff Hub or this bot 😘', aliases=['suggestion'], pass_context=True)
    async def suggest(self, ctx, *, suggestion=None):
        if suggestion == None:
            await ctx.send('You must provide a suggestion')
            return
        for channel in ctx.guild.channels:
            if str(channel).lower() == 'suggestions':
                em = discord.Embed(
                    title=f'Suggestion',
                    description=f'*{suggestion}*',
                    color=discord.Color.blurple()
                )
                em.set_author(
                    name=f'Suggestion from {ctx.author}', icon_url=ctx.author.avatar_url)
                sug = await channel.send(embed=em)
                await sug.add_reaction('👍')
                await sug.add_reaction('👎')

                emb = discord.Embed(
                    description=f'Successfully sent suggestion in <#{channel.id}>',
                    color=discord.Color.green()
                )
                await ctx.send(embed=emb)
                return

        ctx.send('Suggestions channel not found.')


def setup(bot):
    bot.add_cog(Utility(bot))
