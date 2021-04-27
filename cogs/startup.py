import discord, config
from discord.ext import commands

class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=config.activity)
        print('Bot is ready.')

def setup(bot):
    bot.add_cog(Startup(bot))