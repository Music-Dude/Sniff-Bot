import discord, os, config
from datetime import datetime
from discord.ext import commands
from pretty_help import PrettyHelp

bot = commands.Bot(
    command_prefix = '!',
    case_insensitive = True,
    help_command=PrettyHelp(),
    intents=discord.Intents().all()

)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('X'):
        filename = filename[:-3]
        print(f'Loading cog {filename}')
        bot.load_extension(f'cogs.{filename}')

bot.run(config.token)
