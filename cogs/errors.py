import discord
from discord.ext import commands
from pretty_help import PrettyHelp

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        print(err)
        if isinstance(err, commands.errors.NSFWChannelRequired):
            nsfwEmbed = discord.Embed(
                title = "NSFW Command",
                description = err.args[0]
            )
            await ctx.send(embed=nsfwEmbed)
        elif isinstance(err, commands.errors.CommandNotFound):
            em = discord.Embed(
                title='Command not found',
                description='See !help for a list of commands.'
            )
            await ctx.send(embed=em)
        else:
            errorEm = discord.Embed(
                title=f'There was an error executing that command:',
                description=f'```{err}```'
            )
            errorEm.set_footer(text='FIX YOUR BOT, Music_Dude!')
            errorEm.set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/53/cross-mark_274c.png')
            await ctx.send(embed=errorEm)

def setup(bot):
    bot.add_cog(Errors(bot))