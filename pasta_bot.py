"""
# Title: pasta_bot.py
# Author: Thad Shinno
# Description: main bot events and commands
"""

import discord

from discord.ext import tasks, commands
from itertools import cycle

# custom packages
from pasta.events import Events
from pasta.commands import Commands
from mytoken import getToken


TOKEN = getToken()
client = commands.Bot(command_prefix = '.')
events = Events(client)
cmd = Commands(client)
status = events.getStatus()
client.remove_command("help")

"""
EVENTS: on_ready, on_message, and on_member_join
"""
# when the bot starts, change statuses every 5 minutes
@client.event
async def on_ready():
	print("Bot is running")
	changeStatus.start()

# the meat of the program. Send sauce or a copypasta
@client.event
async def on_message(message):
	await events.on_message(message)

# give a warm greeting to the system channel when someone joins
@client.event
async def on_member_join(member):
	await member.guild.system_channel.send("Welcome home, {member}! Would you like dinner? A bath? Or maybe... me?".format(member = member.mention))

"""
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("No such command .{command}\nGet some .help".format(command=ctx.invoked_with))
"""
# change status every 5 minutes
@tasks.loop(minutes = 5)
async def changeStatus():
	await client.change_presence(activity = next(status))

"""
COMMANDS: help, ignore, readme, owo, shutdown, clean, triggers, random, search
"""
# .help [command] (send help message)
@client.command(aliases=["h"])
async def help(ctx, spec=""):
	await cmd.help(ctx, spec)

# .ignore [any message here] (pasta bot ignores these)
@client.command(aliases=["i"])
async def ignore(ctx):
	return

# .readme (DMs README.txt)
@client.command()
async def readme(ctx):
	await cmd.readme(ctx)

# .triggers (DMs a list of trigger words)
@client.command(aliases=["trigger"])
async def triggers(ctx):
	await cmd.triggers(ctx)

# .search [amount] {search criteria} (search top hentai results)
@client.command()
async def search(ctx, *, criteria):
	await cmd.search(ctx, criteria)	

@search.error
async def search_error(ctx, error):
	await ctx.send("My wifi is garbage and can't run HTTP get requests. Pls try again")

# .random [amount] [search criteria] (get random hentai)
@client.command()
async def random(ctx, *, criteria=""):
	await cmd.random(ctx, criteria)

@random.error
async def random_error(ctx, error):
	await ctx.send("My wifi is garbage and can't run HTTP get requests. Pls try again")
	
# .owo [@user_mention] [@user_mention] [...] (owoify messages)
@client.command(aliases=["uwu"])
async def owo(ctx, *members : discord.Member):
	await cmd.owo(ctx, *members) # for some reason the program breaks if I take out the *

# If you get bad arguments, just owoify the last message
@owo.error
async def owo_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await owo(ctx)

# .clean (delete messages by pasta_bot)
@client.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx):
	await cmd.clean(ctx)

@clean.error
async def clean_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("{member} you do not have permissions to manage messages".format(member=ctx.author.mention))

# shutdown
@client.command()
@commands.is_owner()
async def shutdown(ctx):
	await ctx.bot.logout()

client.run(TOKEN)