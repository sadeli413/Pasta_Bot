"""
@author Thad Shinno @Sadeli
main method for pasta_bot, containing events and commands
"""

"""
TODO asap:
	- Change nhentai.fetch(message) command so that it sends one at a time instead of all at once
	- Remove README.txt into README.md
	- .help to send github page with README.md
	- .commands to send command help
TODO Long term:
	- Implement a log for troubleshooting.
	- Use SQL/json to track user's favorite doujin and make recommendations
		.save {numbers} [numbers] ...
		.library
			- this will present a table
		.recommend [amount]
	- Implement "jail" to punish users for searching loli/shota
		- Three strikes and then they're sent to a group Horny_Jail
		- Will recieve a random bible verse once a day for 7 days
		- Extra strikes during jailtime will add an extra day to jailtime
"""

import discord
from discord.ext import tasks, commands
from random import choice
# custom packages
from application.events import Events
from application.commands import Commands
from private import getToken, getID

# tools
client = commands.Bot(command_prefix = '.')
TOKEN = getToken()
OWNER_ID = getID()
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
	greetings = [
		"Welcome home, {member}! Would you like dinner? A bath? Or maybe... me?",
		"Welcome to the guild, {member}! Don't worry, I'm not a pervert, or anyone suspicious. No suspicious people here. None at all.",
		"Hello, {member}. My name is Pasta_Bot. My favorite food is sauce. Please don't forget me."
	]
	await member.guild.system_channel.send(choice(greetings).format(member = member.mention))

# command not found error, and misc erorr
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("No such command .{command}\nGet some .help".format(command=ctx.invoked_with))
	# not MissingPermissions, BadArgument, or MissingRequiredArgument
	elif ((not isinstance(error, commands.MissingPermissions)) and (not isinstance(error, commands.BadArgument))) and (not isinstance(error, commands.MissingRequiredArgument)):
		err = "<@{id}> ```css\nA command error has occured in {channel} from:\n{message}```".format(id=OWNER_ID, channel=ctx.message.guild.name, message=ctx.message.content)
		await ctx.send(err)
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
	await cmd.help(ctx, spec)

# .ignore [any message here] (pasta bot ignores these)
@client.command(aliases=["i"])
async def ignore(ctx):
	return

# .triggers (DMs a list of trigger words)
@client.command(aliases=["trigger"])
async def triggers(ctx):
	await cmd.triggers(ctx)

# .search [amount] {search criteria} (search top hentai results)
# only works in nsfw channels
@client.command()
async def search(ctx, *, criteria):
	await cmd.search(ctx, criteria)	

# error handling
@search.error
async def search_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(".search [amount] {search criteria}\nGet some .help")
	else:
		await ctx.send("My wifi is garbage and can't run HTTP get requests. Pls try again")

# .random [amount] [search criteria] (get random hentai)
# only works in nsfw channels
@client.command()
async def random(ctx, *, criteria=""):
	await cmd.random(ctx, criteria)

# error handling
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

# MissingPermissions error
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