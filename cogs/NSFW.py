import discord, random, requests
from rule34 import Rule34
from discord.ext import commands
from pretty_help import PrettyHelp
from faker import Faker
from insultgenerator import phrases

class NSFW(commands.Cog, description='😏'):
    def __init__(self, bot):
        self.bot = bot
        self.r34 = Rule34(self.bot.loop)

    @commands.command(help='Searches something on Rule34', aliases=['r34'], pass_context=True)
    @commands.is_nsfw()
    async def rule34(self, ctx, *query):
        query = '_'.join(query)
        if not query:
            em = discord.Embed(
                title='Please provide a search query'
            )
            await ctx.send(embed=em)
            return

        posts = await self.r34.getImages(query)
        try:
            post = random.choice(posts).file_url
            while not post.endswith(('png', 'jpg', 'gif')):
                post = random.choice(posts).file_url

            em = discord.Embed(
                title=f'Rule 34 results for \'{query}\''
                )
            em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            em.set_image(url=post)
            await ctx.send(embed=em)
        except TypeError:
            noResults = discord.Embed(
                title = 'No results were found'
            )
            await ctx.send(embed=noResults)


    @commands.command(help='Random hentai GIF')
    @commands.is_nsfw()
    async def hentai(self, ctx):
        r = requests.get("https://nekos.life/api/v2/img/Random_hentai_gif")
        res = r.json()
        hentaiEmbed = discord.Embed(
            title='Random hentai GIF'
        )
        hentaiEmbed.set_image(url=res['url'])
        await ctx.send(embed=hentaiEmbed)

    @commands.command(help='Random neko GIF', aliases=['catgirl'])
    @commands.is_nsfw()
    async def neko(self, ctx):
        r = requests.get("https://nekos.life/api/v2/img/nsfw_neko_gif")
        res = r.json()
        nekoEmbed = discord.Embed(
            title='Random neko GIF'
        )
        nekoEmbed.set_image(url=res['url'])
        await ctx.send(embed=nekoEmbed)
    
def setup(bot):
    bot.add_cog(NSFW(bot))
