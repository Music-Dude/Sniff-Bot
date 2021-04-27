import discord, random, requests
from rule34 import Rule34
from discord.ext import commands
from pretty_help import PrettyHelp
from faker import Faker
from insultgenerator import phrases

class NSFW(commands.Cog, description='😏'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Searches something on Rule34', aliases=['r34'], pass_context=True)
    @commands.is_nsfw()
    async def rule34(self, ctx, *Search_Query):
        r34 = Rule34(self.bot.loop)
        Search_Query = '_'.join(Search_Query)
        if Search_Query == '':
            noSearch = discord.Embed(
                title='Please provide a search query'
            )
            await ctx.send(embed=noSearch)
            return

        posts = await r34.getImages(Search_Query)
        try:
            post = posts[random.randint(0, len(posts) - 1)]
            r34Embed = discord.Embed(
                title=f'Rule 34 results for \'{Search_Query}\''
                )
            r34Embed.set_image(url=post.file_url)
            await ctx.send(embed=r34Embed)

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

    @commands.command(help='Random lewd catgirl GIF', aliases=['catgirl', 'loli'])
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