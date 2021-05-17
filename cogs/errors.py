import discord
from discord.ext import commands
from pretty_help import PrettyHelp


def convert_time(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        print(err)
        if isinstance(err, commands.errors.NSFWChannelRequired):
            nsfwEmbed = discord.Embed(
                title="NSFW Command",
                description=err.args[0],
                color=discord.Color.red()
            )
            await ctx.send(embed=nsfwEmbed)
        elif isinstance(err, commands.errors.CommandNotFound):
            em = discord.Embed(
                title='Command not found',
                description='See !help for a list of commands.'
            )
            await ctx.send(embed=em)
        elif isinstance(err, commands.errors.UserNotFound or commands.errors.MemberNotFound):
            await ctx.send('Couldn\'t find that user!')
        elif isinstance(err, commands.errors.CommandOnCooldown):
            err = int(str(err).replace(
                "You are on cooldown. Try again in ", "")[:-4])

            cooldown_time = convert_time(err)
            await ctx.send(f"This command is on cooldown! Try again in {cooldown_time}")
        else:
            errorEm = discord.Embed(
                title=f'There was an error executing that command:',
                description=f'```{err}```',
                color=discord.Color.red()
            )
            errorEm.set_footer(text='FIX YOUR BOT, Music_Dude!')
            errorEm.set_thumbnail(
                url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/53/cross-mark_274c.png')
            await ctx.send(embed=errorEm)


def setup(bot):
    bot.add_cog(Errors(bot))
