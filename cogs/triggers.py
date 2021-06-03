import discord, random, time, config, re
from discord.ext import commands
from pretty_help import PrettyHelp

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if any(trigger in msg.content for trigger in config.triggers):
            roast = random.choice(open('insults.txt').readlines())
            await msg.channel.send(roast)

        if msg.content.startswith(f'<@!{self.bot.user.id}>'):
            await msg.channel.send(f'Use {config.prefix}help for a list of commands')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.name.startswith('ticket'):
            em = discord.Embed(
                title='If you\'re using an executor that doesn\'t support MT-API (KRNL, Fluxus, etc), try the lite version of the script',
                color = 0x2aa198
            )
            em.add_field(name='Lite Script:', value='```lua\nloadstring(game:HttpGet(\'https://raw.githubusercontent.com/2dgeneralspam1/Sniff-Hub/main/sniff%20hub%20lite\')()```')
            time.sleep(1)
            await channel.send(embed=em)

def setup(bot):
    bot.add_cog(Triggers(bot))
