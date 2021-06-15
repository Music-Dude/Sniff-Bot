import discord

token = 'your token here'
# Your bot token from https://discord.com/developers/applications

prefix = '!'
# Bot will listen for commands starting with this prefix

activity = discord.Activity(name=f'{prefix}help', type=2)
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

roles = {
    'muted': 852498873262932058,
    # Role for muted users
    'verified': 852498873255329828
    # Role to verify users
}

channels = {
    'suggestions': 854173898319855657
    # Channel for you server's suggestions
}
