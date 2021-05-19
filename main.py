import discord
import os
import config
from datetime import datetime
from discord.ext import commands
from pretty_help import PrettyHelp

bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True,
    help_command=PrettyHelp(),
    intents=discord.Intents().all()

)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('X'):
        filename = filename[:-3]
        print(f'Loading cog {filename}')
        bot.load_extension(f'cogs.{filename}')


@bot.event
async def on_ready():
    await bot.change_presence(activity=config.activity)
    print('Bot is ready.')


bot.run(config.token)
