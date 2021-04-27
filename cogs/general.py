import discord, config, random, requests, asyncpraw, os, sys, time
from discord.ext import commands
from pretty_help import PrettyHelp
from faker import Faker
from insultgenerator import phrases

faker = Faker()

class General(commands.Cog, description='General commands for fun'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Absolutely roasts someone. (Don\'t use if easily offended!!!)', pass_context=True)
    async def roast(self, ctx, args = None):
        if args == None: 
            args = ctx.author.mention # make args default to the caller of the command once function is initialized
        roastEmbed=discord.Embed( 
            description=phrases.get_so_insult_with_action_and_target(args, 'they'),
            color = 0xff0000)
        roastEmbed.set_footer(text=f'Roast from {ctx.author.name}')
        await ctx.send(embed = roastEmbed)

    @commands.command(help='Gets bot latency', aliases=['latency'])
    async def ping(self, ctx):
        pingEmbed = discord.Embed(
            title = 'Pinging. . .',
            description = f'{str(round(self.bot.latency, 1))}ms',
            color = 0xffff00
        )
        await ctx.send(embed = pingEmbed)

    @commands.command(help='Reveals someone\'s totally real personal info!!!', pass_context=True)
    async def dox(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author # make args default to the caller of the command once function is initialized
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

    @commands.command(help='I\'m going back to monke', aliases=['monke'])
    async def monkey(self, ctx):
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
        em.set_image(url = post.url)
        em.set_footer(text=f'From r/{subreddit}')
        await ctx.send(embed=em)
        await reddit.close()

    @commands.command(help='Picks an image of Mr. Potato the cat', aliases=['dimden'])
    async def potato(self, ctx):
        em = discord.Embed(title='Mr. Potato cat picture')
        em.set_image(url=random.choice(config.potato))
        em.set_footer(text='Cat is called \"乐乐的土豆\" in Chinese')
        await ctx.send(embed=em)

    @commands.command(help='Gets a user\'s profile picture', aliases=['avatar'])
    async def pfp(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author
        em = discord.Embed(
            title = f'{user}\'s avatar'
        )
        em.set_footer(text=f'Requested by {ctx.author}')
        em.set_image(url=user.avatar_url)
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
        except discord.Forbidden:
            await ctx.reply('server staff are furries????')

        muterole = ctx.guild.get_role(config.mute_role)
        await ctx.author.add_roles(muterole)
        await ctx.author.edit(roles=roles)

    @commands.command(help='Petpet for everyone', aliases=['pet', 'patpat', 'pat'])
    async def petpet(self, ctx):
        data = {
            'Request URL': 'https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png',
            'Referrer Policy': 'strict-origin-when-cross-origin'
            }

        r = requests.post('https://benisland.neocities.org/petpet/', data=data)

def setup(bot):
    bot.add_cog(General(bot))