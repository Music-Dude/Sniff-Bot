import discord, config
from discord.ext import commands
from pretty_help import PrettyHelp

class Utility(commands.Cog, description='Somewhat useful commands'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(help='Gets bot latency', aliases=['latency'])
    async def ping(self, ctx):
        pingEmbed = discord.Embed(
            title = 'Pinging. . .',
            description = f'{round(self.bot.latency, 3)}ms',
            color = discord.Color.gold()
        )
        await ctx.send(embed = pingEmbed)

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

    @commands.command(help='Render text as a PNG image', pass_context=True)
    async def text(self, ctx, *, args=None):
        try:
            args = args.split(',')

            for x, arg in enumerate(args):
                args[x] = arg.strip()

            print(args)

            text = args[0].replace(' ', '%20')

        except:
            await ctx.send('Couldn\'t get an image for that. Make sure everything is formatted like this:\n`!text Your text here, color (hex)`')
            return

        try: 
            if len(args[1]) == 6:
                color = args[1]
        except: color = 'ffffff'

        em = discord.Embed(
            title = 'Generated text'
        )
        em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        url = f'https://lingtalfi.com/services/pngtext?text=%20{text}%20&color={color}&size=100'
        em.set_image(url=url)
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
                em.set_author(name=f'Suggestion from {ctx.author}', icon_url=ctx.author.avatar_url)
                sug = await channel.send(embed=em)
                await sug.add_reaction('👍')
                await sug.add_reaction('👎')

                emb=discord.Embed(
                    description=f'Successfully sent suggestion in <#{channel.id}>',
                    color=discord.Color.green()
                )
                await ctx.send(embed=emb)
                return

        ctx.send('Suggestions channel not found.')

def setup(bot):
    bot.add_cog(Utility(bot))
