import discord, config, random, requests, asyncpraw, os, sys, time, asyncio
from discord.ext import commands
from pretty_help import PrettyHelp
from faker import Faker
from insultgenerator import phrases

faker = Faker()

class Fun(commands.Cog, description='Commands just for fun'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Absolutely roasts someone. (Don\'t use if easily offended!!!)', pass_context=True)
    async def roast(self, ctx, args = None):
        if args == None: 
            args = ctx.author.mention
        roastEmbed=discord.Embed( 
            description=phrases.get_so_insult_with_action_and_target(args, 'they'),
            color = '#ff0000')
        roastEmbed.set_footer(text=f'Roast from {ctx.author.name}')
        await ctx.send(embed = roastEmbed)

    @commands.command(help='Reveals someone\'s totally real personal info!!!', pass_context=True)
    async def dox(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author
        doxEmbed = discord.Embed(
            title = f'{user.name}\'s Personal Info:',
            color = 0x7289da
        )
        doxEmbed.add_field(name='Address', value=faker.address(), inline=False)
        doxEmbed.add_field(name='IP', value=faker.ipv4(), inline=True)
        doxEmbed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=doxEmbed)
        
    @commands.command(help='Gets a random cat picture')
    async def cat(self, ctx):
        req = requests.get(f"https://api.thecatapi.com/v1/images/search?format=json&x-api-key={config.cat_key}")
        r = req.json()
        catEmbed = discord.Embed(title='Cat 🐱')
        em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        catEmbed.set_image(url=str(r[0]["url"]))
        await ctx.send(embed=catEmbed)

    @commands.command(help='Gets a sus image', aliases=['amongus', 'amongdrip', 'sus', 'sussy', 'imposter'])
    async def amogus(self, ctx):
        reddit =  asyncpraw.Reddit(
            client_id = 'z0tV5Vb8-xHnYA',
            client_secret = 'EgmNP1VmT-IpIMj-7auUMM8E0W0',
            user_agent = 'pythonpraw'
        )

        subs = ('amogus', 'schizoamogus', 'amongdrip', 'whentheimposterissus', 'amogusmemes')
        subreddit = await reddit.subreddit(random.choice(subs))
        new = subreddit.new(limit=20)

        posts = [x async for x in new if not x.stickied and x.url.endswith('jpg') or x.url.endswith('png') or x.url.endswith('gif')]
        post = random.choice(posts)
        em = discord.Embed(
            title = post.title,
            url=f'https://reddit.com{post.permalink}'
        )
        em.set_image(url = post.url)
        em.set_footer(text=f'From r/{subreddit}')
        await ctx.send(embed=em)
        await reddit.close()

    @commands.command(help='I\'m going back to monke', aliases=['monkey'])
    async def monke(self, ctx):
        reddit =  asyncpraw.Reddit(
            client_id = 'z0tV5Vb8-xHnYA',
            client_secret = 'EgmNP1VmT-IpIMj-7auUMM8E0W0',
            user_agent = 'pythonpraw'
        )

        subs = ('monke','monkeys')
        subreddit = await reddit.subreddit(random.choice(subs))
        new = subreddit.new(limit=20)

        posts = [x async for x in new if not x.stickied and x.url.endswith('jpg') or x.url.endswith('png') or x.url.endswith('gif')]
        post = random.choice(posts)
        em = discord.Embed(
            title = post.title,
            url=f'https://reddit.com{post.permalink}'
        )
        em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url = post.url)
        em.set_footer(text=f'From r/{subreddit}')
        await ctx.send(embed=em)
        await reddit.close()

    @commands.command(help='Pick a random post from a subreddit', aliases=['subreddit'])
    async def reddit(self, ctx, sub):
        reddit =  asyncpraw.Reddit(
            client_id = 'z0tV5Vb8-xHnYA',
            client_secret = 'EgmNP1VmT-IpIMj-7auUMM8E0W0',
            user_agent = 'pythonpraw'
        )
        try:
            subreddit = await reddit.subreddit(sub)
            hot = subreddit.hot(limit=20)

            posts = [x async for x in hot if not x.stickied and not x.over_18 and x.url.endswith('jpg') or x.url.endswith('png') or x.url.endswith('gif')]
            post = random.choice(posts)
        except: 
            await ctx.send('No results. Make sure the subreddit you are requesting exists and isn\'t NSFW.')
            return

        em = discord.Embed(
            title = post.title,
            url=f'https://reddit.com{post.permalink}'
        )
        em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url = post.url)
        em.set_footer(text=f'From r/{subreddit}')
        await ctx.send(embed=em)
        await reddit.close()

    @commands.command(help='Picks an image of Mr. Potato the cat', aliases=['dimden'])
    async def potato(self, ctx):
        em = discord.Embed(title='Mr. Potato cat picture')
        em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        em.set_image(url=random.choice(config.potato))
        em.set_footer(text='Cat is called \"乐乐的土豆\" in Chinese')
        await ctx.send(embed=em)

    @commands.command(help='Go ahead and try it UwU')
    async def furry(self, ctx):
        roles = []
        for role in ctx.author.roles:
            roles.append(role)

        await ctx.author.send('Furry no rights 🤡')
        try:
            await ctx.author.edit(roles=[])
            await ctx.reply('Furry above me 🤡🤡🤡')
            await asyncio.sleep(5)
        except discord.Forbidden:
            await ctx.reply('server staff are furries????')

        muterole = ctx.guild.get_role(config.mute_role)
        await ctx.author.add_roles(muterole)
        await ctx.author.edit(roles=roles)

    @commands.command(help='Times your typing of words', aliases=['typetest'])
    async def typingtest(self, ctx):
        words = requests.get('http://random-word-api.herokuapp.com/word?number=5').text.split('')
        await ctx.reply(f'https://lingtalfi.com/services/pngtext?text=%20{words}%20&color=000000&size=400')

def setup(bot):
    bot.add_cog(Fun(bot))