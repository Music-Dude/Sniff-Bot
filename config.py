import discord

token = 'your token here'
# Your bot token from https://discord.com/developers/applications

prefix = '!'
# Bot will listen for commands starting with this prefix

activity = discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help')
# Set this to any status the bot should have on start
# Examples:
#    discord.Game(name='a game')                                                          >> Playing a game
#    discord.Streaming(name='stream', url='twitch url')                                   >> Streaming stream
#    discord.Activity(type=discord.ActivityType.listening, name='a song')                 >> Listening to a song
#    discord.Activity(type=discord.ActivityType.watching, name='a video')                 >> Watching a video
#    discord.Activity(type=discord.ActivityType.custom, state='Your custom status')       >> Your custom status

cat_key = ''
# Get an api key from https://thecatapi.com/

triggers = ['@here', '@everyone']
# The bot will respond to any message containing these

ownerID = 123456789
# Put your user id here, lets you reload the bot

mute_role = 123456789
# Specify the muted role in your server
