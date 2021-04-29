import discord, config, colors
from urllib.parse import quote
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
    async def text(self, ctx, *, args='white'):
        try:
            args = args.split(',')

            for x, arg in enumerate(args):
                args[x] = arg.strip()

            text = args[0]

        except:
            await ctx.send('Couldn\'t get an image for that. Make sure everything is formatted like this:\n`!text Your text here, color`')
            return


        color = args[1].lower()
        if color in colors.colors:
            color = colors.colors[color]
            color = str(hex(int(color, 16)))[2:]
            color = '0'*(6-len(color))+color
        em = discord.Embed(
            title = 'Generated text',
            color = int(str(hex(int(color, 16)))[2:], 16)
        )
        em.set_author(name=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        
        url = f'https://lingtalfi.com/services/pngtext?text=%20{quote(text)}%20&color={color}&size=100'
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