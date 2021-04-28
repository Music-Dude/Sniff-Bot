import discord, config, os, sys, time, timeit, asyncio
from discord.ext import commands
from pretty_help import PrettyHelp

class Staff(commands.Cog, description='Admin/moderation commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Reload all of the bot\'s cogs (only Music_Dude can use this)')
    async def reload(self, ctx):
        if ctx.author.id == config.ownerID:
            em=discord.Embed(
                title='Reloading all cogs. . .',
                description='Allow up to 5 seconds',
                color=discord.Color.green()
            )
            msg = await ctx.send(embed=em)
            await self.bot.change_presence(activity=discord.Game(name="Restarting. . ."))
            print('Bot is reloading. . .')
            tic = time.perf_counter()

            for filename in os.listdir('./cogs'):
                if filename.endswith('.py') and not filename.startswith('_'):
                    filename = filename[:-3]
                    print(f'Reloading cog {filename}')
                    em.add_field(name=filename, value=f'Reloaded cog {filename}')
                    self.bot.reload_extension(f'cogs.{filename}')

            toc = time.perf_counter()

            em.add_field(name='Finished reloading bot', value=f'Reloaded all cogs in {toc-tic:0.4f} seconds', inline=False)
            await msg.edit(embed=em)
            await self.bot.change_presence(activity=config.activity)
            print('Bot is back up!')

        else:
            await ctx.send(f'Only <@{config.ownerID}> can use this command to prevent abuse!')

    @commands.command(help='Restart the entire bot (only Music_Dude can use this)')
    async def restart(self, ctx):
        if ctx.author.id == config.ownerID:
            with ctx.typing():
                em=discord.Embed(
                    title='Restarting. . .',
                    description='Allow up to 5 seconds',
                    color=discord.Color.green()
                )
                msg = await ctx.send(embed=em)
                await self.bot.change_presence(activity=discord.Game(name="Restarting. . ."))
                print('Bot is restarting. . .')
                os.execl(sys.executable, 'python3', './main.py', *sys.argv[1:])
            print('Bot is back up!')

        else:
            await ctx.send(f'Only <@{config.ownerID}> can use this command to prevent abuse!')

    @commands.command(help='Steals a custom emoji from another server (WIP)')
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, Emoji: discord.Emoji):
        if not str(Emoji).startswith('<:'):
            await ctx.send(embed=discord.Embed(title='Argument \'Emoji\' must be a custom emoji!'))
            return
        else:
            stealEm = discord.Embed(
                title='Stealing this emoji:'
            )
            stealEm.set_image(url=Emoji.url)
            stealEm.set_footer(text='This command is still a WIP')
            await guild.create_custom_emoji(name=name, image=Image.open(urllib.request.urlopen(Emoji.url)))
            await ctx.send(embed=stealEm)

    @commands.command(help='Changes the bot\'s nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def botnick(self, ctx, *New_Name):
        New_Name = ' '.join(New_Name)
        try:
            await ctx.guild.get_member(self.bot.user.id).edit(nick=New_Name)
            await ctx.send(f'Successfully changed nickname to \"{New_Name}\"')
        except discord.HTTPException:
            await ctx.send('Couldn\'t set nickname to that. Check that the new name is 32 or less characters in length and doesn\'t contain special characters.'
            )

    @commands.command(help='Changes a member\'s nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, user : discord.Member=None, *New_Name):
        if user == None:
            user = ctx.author

        New_Name = ' '.join(New_Name)
        try:
            await user.edit(nick=New_Name)
            await ctx.send(f'Successfully changed {user}\'s nickname to \"{New_Name}\"')
        except discord.Forbidden:
            await ctx.send('I can\'t nickname that user 😢')
        except discord.HTTPException:
            await ctx.send('Couldn\'t set nickname to that. Check that the new name is 32 or less characters in length and doesn\'t contain special characters.')

    @commands.command(help='Mute a member indefinitely', pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member=None):
        if user == None:
            await ctx.send('You must provide a user to mute!')
            return

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            await ctx.send('You are not high enough in the role hierarchy to mute that user!')
            return

        try:
            await user.add_roles(ctx.guild.get_role(config.mute_role))

            em = discord.Embed(
                title=f'✅ Muted {user}',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send('I can\'t mute that user 😢')
    
    @commands.command(help='Mute a member temporarily', pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, user: discord.Member=None, time=None):
        if user == None:
            await ctx.send('You must provide a user to mute!')
            return

        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        if not time[-1] in time_convert:
            await ctx.reply('Please specify a value of s (seconds), m (minutes), h (hours), or d (days)')
            return
        time = int(time[:-1]) * time_convert[time[-1]]

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            await ctx.send('You are not high enough in the role hierarchy to mute that user!')
            return

        try:
            await user.add_roles(ctx.guild.get_role(config.mute_role))

            em = discord.Embed(
                title=f'✅ Muted {user} for {time} seconds',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)

            await asyncio.sleep(time)
            await user.remove_roles(ctx.guild.get_role(config.mute_role))

            em = discord.Embed(
            title=f'✅ {user} was unmuted after {time} seconds',
            color= discord.Color.green()
            )
            await ctx.send(embed=em)

        except discord.Forbidden:
            await ctx.send('I can\'t mute that user 😢')

    @commands.command(help='Unmute a member', pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member=None):
        if user == None:
            await ctx.send('You must provide a user to unmute!')
            return

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            await ctx.send('You are not high enough in the role hierarchy to unmute that user!')
            return

        try:
            await user.remove_roles(ctx.guild.get_role(config.mute_role))

            em = discord.Embed(
                title=f'✅ Unmuted {user}',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send('I can\'t unmute that user 😢')

    @commands.command(help='Kick a member', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member=None, *reason):
        if user == None:
            ctx.send('You must provide a user to kick!')
            return

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            ctx.send('You are not high enough in the role hierarchy to kick that user!')
            return

        try:
            await user.kick(reason=reason)
            em = discord.Embed(
                title=f'✅ Successfully kicked {user}',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send('I can\'t kick that user 😢')

    @commands.command(help='Ban a member temporarily', aliases=['tempyeet'], pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, user: discord.Member=None, time=None, *, reason=None):
        if user == None:
            ctx.send('You must provide a user to ban!')
            return

        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        if not time[-1] in time_convert:
            await ctx.reply('Please specify a value of s (seconds), m (minutes), h (hours), or d (days)')
            return
        time = int(time[:-1]) * time_convert[time[-1]]

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            ctx.send('You are not high enough in the role hierarchy to ban that user!')
            return

        try:
            await user.ban(reason=reason)
            em = discord.Embed(
                title=f'✅ Successfully banned {user} for {time} seconds',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)

            await asyncio.sleep(time)
            await user.unban()

            em = discord.Embed(
                title=f'✅ {user} was unbanned after {time} seconds',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send('I can\'t ban that user 😢')

    @commands.command(help='Ban a member indefinitely', aliases=['yeet'], pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member=None, *reason):
        if user == None:
            ctx.send('You must provide a user to ban!')
            return

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            ctx.send('You are not high enough in the role hierarchy to ban that user!')
            return

        try:
            await user.ban(reason=reason)
            em = discord.Embed(
                title=f'✅ Successfully banned {user}',
                color= discord.Color.green()
            )
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send('I can\'t ban that user 😢')

    @commands.command(help='Unban a member')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user=None):
        if user == None:
            ctx.send('You must provide a user to unban!')
            return

        banned_users = await ctx.guild.bans()
        user_name, user_discrim = user.split('#')

        for banned_user in banned_users:
            banned_user=banned_user.user
            if (banned_user.name, banned_user.discriminator) == (user_name, user_discrim):
                await ctx.guild.unban(banned_user)
                em = discord.Embed(
                    title=f'✅ Successfully unbanned {user}',
                    color= discord.Color.green()
                )
                await ctx.send(embed=em)

    @commands.command(help='Give a user a role', aliases=['giverole'])
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, user: discord.Member=None, *, role=None):
        if user==None:
            await ctx.send('You must provide a role to give that user!')
            return

        if role==None:
            await ctx.send('You must provide a role to give that user!')
            return

        if user.top_role > ctx.author.top_role and ctx.author.id != config.ownerID:
            await ctx.send('You are not high enough in the role hierarchy to change roles for that user!')
            return

        if type(role) == str:
            for server_role in ctx.guild.roles:
                if (str(role)).lower() in str(server_role).lower():
                    role = server_role
        if type(role) == str:
            em=discord.Embed(
                title=f'Role not found',
                description=f'Couldn\'t find a role called \"{role}\".',
                color=discord.Color.red()
            )
            await ctx.send(embed=em)
            return      

        if role in user.roles:
            await user.remove_roles(role)
            em = discord.Embed(
                title=f'Successfully removed role \"{role.name}\" from {user.name}!',
                color=discord.Color.red()
            )
            await ctx.send(embed=em)
        else:
            await user.add_roles(role)
            em = discord.Embed(
                title=f'Successfully gave role \"{role.name}\" to {user.name}!',
                color=discord.Color.green()
            )
            await ctx.send(embed=em)

    @commands.command(help='Clone a channel, preserving configuration')
    @commands.has_permissions(manage_channels=True)
    async def clone(self, ctx, channel: discord.TextChannel=None, *, name=None):
        if channel == None:
            channel=ctx.channel
        if name == None:
            name = f'{channel.name} clone'

        pos = channel.position
        new_channel = await channel.clone(name=name)
        await new_channel.edit(position=pos)
        em = discord.Embed(
            description=f'Cloned <#{channel.id}>, creating <#{new_channel.id}>',
            color=discord.Color.green()
        )
        await ctx.send(embed=em)

    @commands.command(help='Clears a channel\'s messages', aliases=['clear', 'wipe'])
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, channel: discord.TextChannel=None):
        confirm = await ctx.send('Are you sure? All messages in this channel will be deleted. React with 💣 if you\'d like to continue.')
        await confirm.add_reaction('💣')
        time.sleep(3)
        confirm = await ctx.fetch_message(confirm.id)

        for reaction in confirm.reactions:
            async for usr in reaction.users():
                if usr == ctx.author:
                    if channel == None:
                        channel = ctx.channel
                    pos = channel.position
                    new_channel = await channel.clone()
                    await new_channel.edit(position=pos)
                    await channel.delete(reason=f'Channel nuked by {ctx.author}')
                    em = discord.Embed(
                        title=f'Channel was nuked by {ctx.author}',
                        color=0xffc233
                    )
                    em.set_image(url='https://media1.tenor.com/images/2f7f0bcfad94c2ee68c2d8357b255728/tenor.gif')
                    em.set_thumbnail(url='https://images.emojiterra.com/twitter/512px/1f4a3.png')
                    await new_channel.send(embed=em)

    @commands.command(help='Delete a channel', aliases=['del'])
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, channel: discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        confirm = await ctx.send(f'<#{channel.id}> will be deleted. React with 💣 if you\'d like to continue.')
        await confirm.add_reaction('💣')
        time.sleep(3)
        confirm = await ctx.fetch_message(confirm.id)

        for reaction in confirm.reactions:
            async for usr in reaction.users():
                if usr == ctx.author:
                    await channel.delete(reason=f'Channel deleted by {ctx.author}')
                    em = discord.Embed(
                        title=f'✅ Successfully deleted <#{channel.id}>',
                        color=discord.Color.green()
                    )
                    try:
                        await ctx.send(embed=em)
                    except:
                        await ctx.author.send(embed=em)

        await confirm.delete()


def setup(bot):
    bot.add_cog(Staff(bot))
