import discord

token = 'your token here'

activity = discord.Activity(name='credit card fraud', type=1)
# set this to any status the bot should have on start

cat_key = ''
# get an api key from https://thecatapi.com/

potato = ['https://media1.tenor.com/images/af0c1fbd64d3a24bd454cf0e50dcb3d4/tenor.gif?itemid=20953756', 'https://media1.tenor.com/images/cad60d9c9427ed6b8db6e26778a40e91/tenor.gif?itemid=20953754', 'https://media1.tenor.com/images/0afdc9999484200b48f51f8d7c6c5c94/tenor.gif?itemid=20953751', 'https://media1.tenor.com/images/83c072802cbd626015e5f739075753fa/tenor.gif?itemid=20953748', 'https://media1.tenor.com/images/dcdd994e78ffc80faca49d4959ebe837/tenor.gif?itemid=19689300', 'https://media1.tenor.com/images/567b40bf5dc37b907420dbaa3782ea4d/tenor.gif?itemid=20953747', 'https://media1.tenor.com/images/45402a6919b6182250c66e4113c05ebd/tenor.gif?itemid=20953746', 'https://media1.tenor.com/images/bfbbfd0e11a3f33821d71579defda54a/tenor.gif?itemid=20953745', 'https://media1.tenor.com/images/a70e6246273860a9f3cf43283bbe2523/tenor.gif?itemid=19689288', 'https://media1.tenor.com/images/437f788fab20c1d708c0f3e0bcc6448e/tenor.gif?itemid=19689294', 'https://media1.tenor.com/images/f106fd446b1b0978f96f892dc3d3a6dd/tenor.gif?itemid=19689292', 'https://media1.tenor.com/images/aa870ef09c0b89cc4f3a74cc01e55a1f/tenor.gif?itemid=19689290', 'https://media1.tenor.com/images/f26e3126802165b3088d8b526063cd97/tenor.gif?itemid=19689283', 'https://media1.tenor.com/images/de438fb609374da17b0b25644ec0bcd7/tenor.gif?itemid=19689286', 'https://media1.tenor.com/images/c7aa9300dd2fc16c11b6ac0a6a64f07e/tenor.gif?itemid=19689282', 'https://media1.tenor.com/images/0dbaf2e1d9d504828df0c1bbcfd9300b/tenor.gif?itemid=19689259', 'https://media1.tenor.com/images/769e4bc3be00b154f2a32b755aedc28a/tenor.gif?itemid=19689255', 'https://media1.tenor.com/images/ee24388442b470f498f555b9786323fc/tenor.gif?itemid=19689257', 'https://media1.tenor.com/images/d7bca344922ccc0c011f0c24b1f43b8b/tenor.gif?itemid=19689251', 'https://media1.tenor.com/images/4de7a4fb914f6abd9922c100b2c53f27/tenor.gif?itemid=19689253', 'https://media1.tenor.com/images/465ac9e91aa93e4cbe4d7a48a9eab99e/tenor.gif?itemid=19689248', 'https://media1.tenor.com/images/be8c3871d26f49f44584c3c880f5b3be/tenor.gif?itemid=19689250', 'https://media1.tenor.com/images/8b16a56c7be496f9c950dbf2f6df29f8/tenor.gif?itemid=19689244', 'https://media1.tenor.com/images/16d897e93b54ad929904bbf0854dd3f0/tenor.gif?itemid=19689220', 'https://media1.tenor.com/images/5b581c9491d5ffd4e414a755b3ad36e3/tenor.gif?itemid=19689219', 'https://media1.tenor.com/images/98606a2ceb0017c5dcc1cf681a8d5c68/tenor.gif?itemid=19689218', 'https://media1.tenor.com/images/9b3326f7269147838f52b6b2588a92e9/tenor.gif?itemid=19689215', 'https://media1.tenor.com/images/0e74f6f4b4f124796df9d170d7eaaab2/tenor.gif?itemid=19662495', 'https://media1.tenor.com/images/9f8729736042cdf9d7ab9447021f949e/tenor.gif?itemid=19662499', 'https://media1.tenor.com/images/6dd2548599b23f5c95478b889ba7f287/tenor.gif?itemid=19689285', 'https://media1.tenor.com/images/2da0f116ec3d3c639c3a2fd37966732f/tenor.gif?itemid=19689226', 'https://media.tenor.com/images/016a468377e27c522fc5b673cd50ac35/tenor.gif']

triggers = ['@here', '@everyone']
# the bot will respond to any message containing these

ownerID = 123456789
# put your user id here, owner lets you use reload cmd

mute_role = 123456789
# specify the muted role in your server
