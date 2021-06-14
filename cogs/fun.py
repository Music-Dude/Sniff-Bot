import discord
import config
import random
import requests
import asyncpraw
import re
import time
import asyncio
from discord.ext import commands
from pretty_help import PrettyHelp
from faker import Faker
from insultgenerator import phrases

faker = Faker()


class Fun(commands.Cog, description='Commands just for fun'):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id='z0tV5Vb8-xHnYA',
            client_secret='EgmNP1VmT-IpIMj-7auUMM8E0W0',
            user_agent='Sniff Bot'
        )

    @commands.command(help='Absolutely roasts someone. (Don\'t use if easily offended!!!)', pass_context=True)
    async def roast(self, ctx, args=None):
        if args == None:
            args = ctx.author.mention
        roastEmbed = discord.Embed(
            description=phrases.get_so_insult_with_action_and_target(
                args, 'they'),
            color=discord.Color.red()
        )
        roastEmbed.set_footer(text=f'Roast from {ctx.author.name}')
        await ctx.send(embed=roastEmbed)

    @commands.command(help='Reveals someone\'s totally real personal info!!!', pass_context=True)
    async def dox(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        doxEmbed = discord.Embed(
            title=f'{user.name}\'s Personal Info:',
            color=0x7289da
        )
        doxEmbed.add_field(name='Address', value=faker.address(), inline=False)
        doxEmbed.add_field(name='IP', value=faker.ipv4(), inline=True)
        doxEmbed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=doxEmbed)

    @commands.command(help='Gets a random cat picture')
    async def cat(self, ctx):
        req = requests.get(
            f"https://api.thecatapi.com/v1/images/search?format=json&x-api-key={config.cat_key}")
        r = req.json()
        em = discord.Embed(title='Cat 🐱')
        em.set_author(
            name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url=str(r[0]["url"]))
        await ctx.send(embed=em)

    @commands.command(help='Pick a random post from a subreddit', aliases=['subreddit'])
    async def reddit(self, ctx, sub):
        r = requests.get(
            f'https://reddit.com/r/{sub}.json', headers={'user-agent': 'Sniff Bot'}).text

        try:
            is_nsfw = re.search(
                r'(?<=over_18": ).+?(?=,)', r).group() == 'true'
        except AttributeError:
            await ctx.reply(embed=discord.Embed(title='That subreddit doesn\'t exist!', description=f'r/{sub} not found.', color=0xff0000))
            return

        subreddit = await self.reddit.subreddit(sub)

        if is_nsfw and not ctx.channel.is_nsfw():
            raise commands.errors.NSFWChannelRequired(ctx.channel)
        hot = subreddit.hot(limit=20)

        posts = [x async for x in hot if not x.stickied and x.url.lower().endswith(('jpg', 'png', 'gif'))]

        post = random.choice(posts)

        em = discord.Embed(
            title=post.title,
            color=0xFF5700,
            url=f'https://reddit.com{post.permalink}'
        )
        em.set_author(
            name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url=post.url)
        em.set_footer(text=f'From r/{subreddit}')
        await ctx.send(embed=em)

    @commands.command(help='Picks an image of Mr. Potato the cat', aliases=['乐乐的土豆'])
    async def potato(self, ctx):
        em = discord.Embed(title='Mr. Potato cat picture', color=0xc4beb1)
        em.set_author(
            name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url=random.choice(('https://media1.tenor.com/images/af0c1fbd64d3a24bd454cf0e50dcb3d4/tenor.gif?itemid=20953756', 'https://media1.tenor.com/images/cad60d9c9427ed6b8db6e26778a40e91/tenor.gif?itemid=20953754', 'https://media1.tenor.com/images/0afdc9999484200b48f51f8d7c6c5c94/tenor.gif?itemid=20953751', 'https://media1.tenor.com/images/83c072802cbd626015e5f739075753fa/tenor.gif?itemid=20953748', 'https://media1.tenor.com/images/dcdd994e78ffc80faca49d4959ebe837/tenor.gif?itemid=19689300', 'https://media1.tenor.com/images/567b40bf5dc37b907420dbaa3782ea4d/tenor.gif?itemid=20953747', 'https://media1.tenor.com/images/45402a6919b6182250c66e4113c05ebd/tenor.gif?itemid=20953746', 'https://media1.tenor.com/images/bfbbfd0e11a3f33821d71579defda54a/tenor.gif?itemid=20953745', 'https://media1.tenor.com/images/a70e6246273860a9f3cf43283bbe2523/tenor.gif?itemid=19689288', 'https://media1.tenor.com/images/437f788fab20c1d708c0f3e0bcc6448e/tenor.gif?itemid=19689294', 'https://media1.tenor.com/images/f106fd446b1b0978f96f892dc3d3a6dd/tenor.gif?itemid=19689292', 'https://media1.tenor.com/images/aa870ef09c0b89cc4f3a74cc01e55a1f/tenor.gif?itemid=19689290', 'https://media1.tenor.com/images/f26e3126802165b3088d8b526063cd97/tenor.gif?itemid=19689283', 'https://media1.tenor.com/images/de438fb609374da17b0b25644ec0bcd7/tenor.gif?itemid=19689286', 'https://media1.tenor.com/images/c7aa9300dd2fc16c11b6ac0a6a64f07e/tenor.gif?itemid=19689282', 'https://media1.tenor.com/images/0dbaf2e1d9d504828df0c1bbcfd9300b/tenor.gif?itemid=19689259',
                     'https://media1.tenor.com/images/769e4bc3be00b154f2a32b755aedc28a/tenor.gif?itemid=19689255', 'https://media1.tenor.com/images/ee24388442b470f498f555b9786323fc/tenor.gif?itemid=19689257', 'https://media1.tenor.com/images/d7bca344922ccc0c011f0c24b1f43b8b/tenor.gif?itemid=19689251', 'https://media1.tenor.com/images/4de7a4fb914f6abd9922c100b2c53f27/tenor.gif?itemid=19689253', 'https://media1.tenor.com/images/465ac9e91aa93e4cbe4d7a48a9eab99e/tenor.gif?itemid=19689248', 'https://media1.tenor.com/images/be8c3871d26f49f44584c3c880f5b3be/tenor.gif?itemid=19689250', 'https://media1.tenor.com/images/8b16a56c7be496f9c950dbf2f6df29f8/tenor.gif?itemid=19689244', 'https://media1.tenor.com/images/16d897e93b54ad929904bbf0854dd3f0/tenor.gif?itemid=19689220', 'https://media1.tenor.com/images/5b581c9491d5ffd4e414a755b3ad36e3/tenor.gif?itemid=19689219', 'https://media1.tenor.com/images/98606a2ceb0017c5dcc1cf681a8d5c68/tenor.gif?itemid=19689218', 'https://media1.tenor.com/images/9b3326f7269147838f52b6b2588a92e9/tenor.gif?itemid=19689215', 'https://media1.tenor.com/images/0e74f6f4b4f124796df9d170d7eaaab2/tenor.gif?itemid=19662495', 'https://media1.tenor.com/images/9f8729736042cdf9d7ab9447021f949e/tenor.gif?itemid=19662499', 'https://media1.tenor.com/images/6dd2548599b23f5c95478b889ba7f287/tenor.gif?itemid=19689285', 'https://media1.tenor.com/images/2da0f116ec3d3c639c3a2fd37966732f/tenor.gif?itemid=19689226', 'https://media.tenor.com/images/016a468377e27c522fc5b673cd50ac35/tenor.gif')))
        em.set_footer(text='Cat is called \"乐乐的土豆\" in Chinese')
        await ctx.send(embed=em)

    @commands.command(help='Go ahead and try it UwU')
    async def furry(self, ctx):
        roles = ctx.author.roles

        await ctx.author.send('kys furry')
        await ctx.reply('kys furry')
        try:
            await ctx.author.edit(roles=[])
            await asyncio.sleep(10)
        except discord.Forbidden:
            await ctx.reply('omg furry!!!')

        muterole = ctx.guild.get_role(config.mute_role)
        await ctx.author.add_roles(muterole)
        await ctx.author.edit(roles=roles)

    def check_author(self, author):
        def inner_check(message):
            return message.author == author
        return inner_check

    @commands.command(help='Times your typing of words', aliases=['typetest', 'type'])
    async def typingtest(self, ctx):
        words = '‎ '.join(requests.get(
            'http://random-word-api.herokuapp.com/word?number=5').json())

        wordmsg = await ctx.send(f'Type these words as fast as you can:\n`{words}`')

        try:
            tic = time.perf_counter()
            msg = await self.bot.wait_for('message', check=self.check_author(ctx.author), timeout=30)
        except asyncio.TimeoutError:
            await wordmsg.edit(content='Sorry, you took too long to type.')
            return

        words = words.replace('‎', '')

        if '‎' in msg.content:
            await ctx.send('Stop trying to copy paste, bruh')
            return

        if msg.content == words:
            speed = time.perf_counter()-tic

            em = discord.Embed(
                title='You win!',
                description=f'You typed the words in {speed:0.2f} seconds, at a speed of {300/speed:0.2f} words per minute.',
                color=discord.Color.green()
            )

            await msg.reply(embed=em)
        else:
            em = discord.Embed(title='Try again', color=discord.Color.red())
            em.add_field(name='You typed:', value=f'```{msg.content}```')
            em.add_field(name='and should have typed:',
                         value=f'```{words}```', inline=False)
            await msg.reply(embed=em)

    @commands.command(help='Snipe the last deleted message')
    async def snipe(self, ctx):
        if self.bot.snipedMessage:
            content = self.bot.snipedMessage.content
            author = self.bot.snipedMessage.author
            timestamp = str(self.bot.snipedMessage.created_at
                            ).split('.')[0] + 'UTC'

            em = discord.Embed(
                color=discord.Color.random()
            )
            em.set_author(
                name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            em.add_field(name='Sniped Message', value=f'{content}')
            em.set_footer(text=f'{author}, at {timestamp}',
                          icon_url=author.avatar_url)

            await ctx.send(embed=em)
        else:
            await ctx.send('No message to snipe!')


def setup(bot):
    bot.add_cog(Fun(bot))
