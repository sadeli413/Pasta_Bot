# @author Thad Shinno (Sadeli)
"""
main method for pasta_bot, containing events and commands
"""

"""
TODO asap:
	- make a pasta_bot server to report bugs
	- file i/o error handling
	- BotMissingPermissions error handling
TODO Long term:
	- Use SQL/json to track user's favorite doujin and make recommendations
		.save {numbers} [numbers] ...
		.library
			- this will present a table
		.recommend [amount]
	- Implement "horny jail" to punish users for searching loli/shota
		- Three strikes and then they're sent to a group Horny_Jail
		- Will recieve a random bible verse once a day for 7 days
		- Extra strikes during jailtime will add an extra day to jailtime
	- Implement a noodle command to noodlefy images
		- can noodlefy image attachments
		- or noodlefy @mentioned author's profile pics
"""

import discord
from discord.ext import tasks, commands
from random import choice
# custom packages
from application.events import Events
from application.commands import Commands
from application.helpers.misc import timestamp
from private import getToken, getID

# tools
client = commands.Bot(command_prefix = '.') # the bot itself
TOKEN = getToken() # bot token
OWNER_ID = getID() # owner's discord id
events = Events(client) # on message events
cmd = Commands(client) # bot commands
status = events.getStatus() # bot statuses
client.remove_command("help") # remove default help command. I replaced it with a custom one.

"""
EVENTS: on_ready, on_message, and on_member_join
"""
# when the bot starts, change statuses every 5 minutes
@client.event
async def on_ready():
	print("Pasta_Bot version 0.0.0 by Sadeli")
	timestamp()
	changeStatus.start()

# the meat of the program. Send sauce or a copypasta
@client.event
async def on_message(message):
	await events.on_message(message)

# give a warm greeting to the system channel when someone joins
@client.event
async def on_member_join(member):
	greetings = [
		"Welcome home, {member}! Would you like dinner? A bath? Or maybe... me?",
		"Welcome to the guild, {member}! Don't worry, I'm not a pervert, or anyone suspicious. No suspicious people here. None at all.",
		"Hello, {member}. My name is Pasta_Bot. My favorite food is sauce. Please don't forget me."
	]
	await member.guild.system_channel.send(choice(greetings).format(member = member.name))

# command not found error, and misc erorr
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		return
	# not MissingPermissions, BadArgument, or MissingRequiredArgument
	elif (isinstance(error, commands.BotMissingPermissions)):
		await ctx.send("Sorry, Pasta_Bot is missing misc permisisons")
	elif ((not isinstance(error, commands.MissingPermissions)) and (not isinstance(error, commands.BadArgument)) and (not isinstance(error, commands.MissingRequiredArgument))):
		if isinstance(ctx.channel, discord.DMChannel):
			guild = ctx.author.name + "'s DM channel."
			channel = ""
		else:
			guild = ctx.message.guild.name
			channel = ctx.channel.name
			
		err = "```css\nA misc command error has occured in guild {guild} in channel {channel} from:\n{message}```".format(guild=guild, channel=channel, message=ctx.message.content)
		OWNER = client.get_user(OWNER_ID)
		await OWNER.send(err)

# change status every 5 minutes
@tasks.loop(minutes = 5)
async def changeStatus():
	await client.change_presence(activity = next(status))

"""
COMMANDS: help, ignore, owo, shutdown, clean, triggers, random, search
"""
# .help [command] (send help message)
@client.command(aliases=["h"])
async def help(ctx, spec=""):
	try:
		await cmd.help(ctx, spec)
	except discord.Forbidden:
		await ctx.send("Sorry, Pasta_Bot is missing some permissions in this channel.")

# .ignore [any message here] (pasta bot ignores these)
@client.command(aliases=["i"])
async def ignore(ctx):
	return

# .triggers (DMs a list of trigger words)
@client.command(aliases=["trigger"])
async def triggers(ctx):
	try:
		await cmd.triggers(ctx)
	except discord.Forbidden:
		await ctx.send("Sorry, Pasta_Bot is missing some permissions in this channel.")

# .search [amount] {search criteria} (search top hentai results)
# only works in nsfw channels
@client.command()
async def search(ctx, *, criteria):
	try:
		await cmd.search(ctx, criteria)	
	except discord.Forbidden:
		await ctx.send("Sorry, Pasta_Bot is missing some permissions in this channel.")
	except discord.HTTPException:
		await ctx.send("My wifi is garbage and can't run HTTP get requests. Pls try again")

# error handling
@search.error
async def search_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(".search [amount] {search criteria}\nGet some .help")
	else:
		cmd.giveError(ctx, OWNER_ID)

# .random [amount] [search criteria] (get random hentai)
# only works in nsfw channels
@client.command()
async def random(ctx, *, criteria=""):
	try:
		await cmd.random(ctx, criteria)
	except discord.Forbidden:
		await ctx.send("Sorry, Pasta_Bot is missing some permissions in this channel.")
	except discord.HTTPException:
		await ctx.send("My wifi is garbage and can't run HTTP get requests. Pls try again")

@random.error
async def random_error(ctx, error):
	cmd.giveError(ctx, error, OWNER_ID)

# .owo [@user_mention] [@user_mention] [...] (owoify messages)
@client.command(aliases=["uwu"])
async def owo(ctx, *members : discord.Member):
	try:
		await cmd.owo(ctx, *members) # for some reason the program breaks if I take out the *
	except discord.Forbidden:
		await ctx.send("Sorry, Pasta_Bot is missing some permissions in this channel")

# If you get bad arguments, just owoify the last message
@owo.error
async def owo_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await owo(ctx)
	else:
		giveError(ctx, error, OWNER_ID)

# .clean (delete messages by pasta_bot)
@client.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx):
	try:
		await cmd.clean(ctx)
	except discord.Forbidden:
		await ctx.send("Sorry, Pasta_Bot is missing permissions for this action")

# MissingPermissions error
@clean.error
async def clean_error(ctx, error):
	if (isinstance(error, commands.MissingPermissions)):
		await ctx.send("{member} you do not have permissions to manage messages".format(member=ctx.author.name))
	else:
		giveError(ctx, error, OWNER_ID)

# broadcast to all servers
@client.command()
@commands.is_owner()
async def broadcast(ctx, *, announcement):
	await cmd.broadcast(announcement)

# implement basic log
@client.command()
@commands.is_owner()
async def log(ctx):
	OWNER = client.get_user(OWNER_ID)
	logfile = []
	for guild in client.guilds:
		logfile.append(guild.name)
	await OWNER.send(", ".join(logfile))

# shutdown
@client.command()
@commands.is_owner()
async def shutdown(ctx):
	await ctx.bot.logout()

client.run(TOKEN)