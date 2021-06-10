import discord

token = 'your token here'
# Your bot token from https://discord.com/developers/applications

prefix = '!'
# Bot will listen for commands starting with this prefix

activity = discord.Activity(type=2, name=f'{prefix}help')
# Set this to any status the bot should have on start
# Types:
#   1 - Playing ...
#   2 - Listening to ...
#   3 - Watching ...
#   4 - Streaming (you can set url='') ...
#   5 - Competing in ...

cat_key = ''
# Get an api key from https://thecatapi.com/

triggers = ['@here', '@everyone']
# The bot will respond to any message containing these

ownerID = 123456789
# Put your user id here, lets you reload the bot

mute_role = 123456789
# Specify the muted role in your server
