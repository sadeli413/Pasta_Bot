# @author Sadeli
"""
Owo command helpers
"""
import discord
# custom package
from application.helpers.misc import isCommand

# cursed
def owoify(words):
	return words.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
	
# owoify the last non-command message in ctx.channel
async def noMember(ctx):	
	allMessages = await ctx.channel.history(limit=20).flatten()
	for message in allMessages:
		# owoify the first non-command
		if not isCommand(message.content):
			curse = owoify(message.content)
			if len(curse) > 0:
				await ctx.send(curse)
				return
	
# owoify the last non-command messages sent by *members in the ctx.channel
async def yesMember(ctx, *members : discord.Member):
	# owoify last messages only from members
	allMessages = await ctx.channel.history(limit=200).flatten()
	for member in members:
		curse = getMessage(allMessages, member) # get user's last message and owoify it
		if len(curse) > 0:
			await ctx.send(curse)

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
				return owoify(message.content)
	
	return ""
