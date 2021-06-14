import discord
import random
import time
import config
import re
from discord.ext import commands
from pretty_help import PrettyHelp


class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.snipedMessage = ''

    @commands.Cog.listener()
    async def on_message(self, msg):
        if any(trigger in msg.content for trigger in config.triggers):
            roast = random.choice(open('insults.txt').readlines())
            await msg.channel.send(roast)

        if msg.content.startswith(f'<@!{self.bot.user.id}>'):
            await msg.channel.send(f'Use {config.prefix}help for a list of commands')

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        self.bot.snipedMessage = msg


def setup(bot):
    bot.add_cog(Triggers(bot))
