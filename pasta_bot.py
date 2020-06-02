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

# change status every 5 minutes
@tasks.loop(minutes = 5)
async def changeStatus():
	await client.change_presence(activity = next(status))

"""
COMMANDS: ignore, readme, triggers, owo, clean, shutdown
"""
# pasta_bot will ignore messages beginning with .ignore
@client.command(aliases=["i"])
async def ignore(ctx):
	return

# DM readme.txt
@client.command()
async def readme(ctx):
	await cmd.readme(ctx)

# DM a list of trigger words
@client.command()
async def triggers(ctx):
	await cmd.triggers(ctx)

"""
currently broken
"""
@client.command()
async def search(ctx, *, criteria):
	await cmd.search(ctx, criteria)	

@search.error
async def search_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("ur bad, get some .help")
	else:
		await ctx.send("||An HTTP Exception occured. Basically, Pasta_Bot runs on Thad's computer and his wifi is garbage. Pls try again.||")

@client.command()
async def random(ctx, *, criteria):
	await cmd.random(ctx, criteria)

@random.error
async def random_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await cmd.random(ctx, "")
	else:
		await ctx.send("||An HTTP Exception occured. Basically, Pasta_Bot runs on Thad's computer and his wifi is garbage||")

# owoify member's last non-command message in channel
@client.command(aliases=["uwu"])
async def owo(ctx, *members : discord.Member):
	await cmd.owo(ctx, *members) # for some reason the program breaks if I take out the *

# handle owo errors
@owo.error
async def owo_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await owo(ctx)

# delete messages by pasta_bot
@client.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx):
	await cmd.clean(ctx)

# handle clean errors	
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