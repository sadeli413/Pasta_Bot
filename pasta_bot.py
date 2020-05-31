"""
# Title: pasta_bot.py
# Author: Thad Shinno
# Description: main bot method
"""

import discord
import requests

from Nhentai import Nhentai
from Copypasta import Copypasta
from Extrapasta import Extrapasta
from Token import getToken

from discord.ext import tasks, commands
from itertools import cycle

#TODO: make the bot only available on nsfw channels
def main():
	TOKEN = getToken()
	client = commands.Bot(command_prefix = '.')
	status = cycle(Activities())
	
	# when the bot starts, change statuses every 5 minutes
	@client.event
	async def on_ready():
		print("Bot is running")
		changeStatus.start()
	
	# change status every 5 minutes
	@tasks.loop(minutes = 5)
	async def changeStatus():
		await client.change_presence(activity = next(status))
	
	# the meat of the program
	@client.event
	async def on_message(message):
		# ignore pasta_bot
		if isBot(message):
			return
		
		content = message.content.lower()
		if not isCommand(content):
			# check for sauce
			sauces = Nhentai.getSauces(content)
			if len(sauces) > 0:
				# if there's more than 3, then tell them thats a lot
				if len(sauces) > 3:
					await message.channel.send(Extrapasta.tooMuchHentai())
				# give all the sauce
				for sauce in sauces:
					await message.channel.send(embed = sauce)
				# notify if there are loli or shota tags
				if len(Nhentai.illegals) > 0:
					fbi = Extrapasta.fbiOpenUp() + "\n"
					for title in Nhentai.illegals:
						fbi += "- *{title}*  ({numbers})\n".format(title=title, numbers = Nhentai.illegals.get(title))
					await message.channel.send(fbi)
				print("done fetching")
			# if there's no sauce, give a copypasta instead
			else:	
				response = Extrapasta.sealResponse(content)
				if len(response) > 0:
					await message.channel.send(response)
				# otherwise, respond to pasta normally
				else:
					pasta = Copypasta.getPasta(content)
					if len(pasta) > 0:
						await message.channel.send(pasta)
		
		# let the bot process commands
		await client.process_commands(message)
	
	# give a warm greeting to the system channel when someone joins
	@client.event
	async def on_member_join(member):
		await member.guild.system_channel.send("Welcome home, {member}! Would you like dinner? A bath? Or maybe... me?".format(member = member.mention))
	
	@client.command(aliases=["i"])
	async def ignore(ctx):
		return
	
	@client.command()
	async def readme(ctx):
		await ctx.author.send("Description of Pasta_Bot", file=discord.File("README.txt"))
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	@client.command()
	async def triggers(ctx):
		triggerList = Copypasta.getTriggers()
		triggers = "These are the following trigger words:\n"
		for i in range(len(triggerList)):
			triggers += "{num}) {trigger}\n".format(num=i+1, trigger=triggerList[i])
		await ctx.author.send(triggers)
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
		
	# owoify member's last non-command message in channel
	@client.command(aliases=["uwu"])
	async def owo(ctx, *members : discord.Member):
		# if no members are given, then just owoify last valid message
		if len(members) < 1: 
			allMessages = await ctx.channel.history(limit=20).flatten()
			for message in allMessages:
				# owoify the first non-command
				if not isCommand(message.content):
					return await ctx.send(Extrapasta.owoify(message.content))
		else:
			# else if members are given, then owoify last messages only from those members
			allMessages = await ctx.channel.history(limit=200).flatten()
			for member in members:
				await ctx.send(getMessage(allMessages, member))
	
	@owo.error
	async def owo_error(ctx, error):
		if isinstance(error, commands.BadArgument):
			await owo(ctx)
	
	@client.command()
	@commands.has_permissions(manage_messages=True)
	async def clean(ctx):
		deleted = await ctx.channel.purge(limit = 200, check=isBot)
		await ctx.send('Deleted {num} message(s)'.format(num = len(deleted)))
	
	@clean.error
	async def clean_error(ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("{member} you do not have permissions to manage messages".format(member=ctx.author.mention))
	
	def isBot(message):
		return message.author == client.user
	
	@client.command()
	@commands.is_owner()
	async def shutdown(ctx):
		await ctx.bot.logout()
	
	"""
	@shutdown.error
	async def shutdown_error(ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("Now listen here, you little shit {member} You think you can just .shutdown me? Fuck you. reported. dumbass. useless. bet ur pp hella smol".format(ctx.author.mention))
	"""
	# run the bot
	client.run(TOKEN)

# accepts an array of messages and a member and returns which one belongs to the member. if none, then return ""
def getMessage(messages, member):
	# gets member's last messages
	userMessages = []
	for message in messages:
		if message.author == member:
			userMessages.append(message)
	
	# owoify member's last non-command message
	if len(userMessages) > 0:		
		for message in userMessages:
			if not isCommand(message.content):
				return Extrapasta.owoify(message.content)
	
	return ""

# array of all the bot's activities
def Activities():
	activities = []
	activities.append(discord.Activity(name = "lots of hentai.", type = discord.ActivityType.watching))
	activities.append(discord.Activity(name = "sad loli asmr.", type = discord.ActivityType.listening))
	return activities

def isCommand(content):
	commands = [".ignore", ".owo", ".uwu", ".shutdown", ".clean", ".readme", ".help", ".triggers", ".i"]
	for command in commands:
		if content.startswith(command):
			return True
	return False
	
if __name__ == "__main__":
	main()