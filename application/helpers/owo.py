# @author Sadeli
"""
Owo command helpers
"""
import discord
# custom package
from application.helpers.misc import isCommand

class Owo:
	def __init__(self):
		pass
	
	# owoify the last non-command message in ctx.channel
	async def noMember(self, ctx):	
		allMessages = await ctx.channel.history(limit=20).flatten()
		for message in allMessages:
			# owoify the first non-command
			if not isCommand(message.content):
				owoify = self.owoify(message.content)
				if len(owoify) > 0:
					await ctx.send(owoify)
					return
		
	# owoify the last non-command messages sent by *members in the ctx.channel
	async def yesMember(self, ctx, *members : discord.Member):
		# owoify last messages only from members
		allMessages = await ctx.channel.history(limit=200).flatten()
		for member in members:
			owoify = self.getMessage(allMessages, member)
			if len(owoify) > 0:
				await ctx.send(owoify)
	
	# accepts an array of messages and a member and returns which one belongs to the member. if none, then return ""
	def getMessage(self, messages, member):
		# gets member's last messages
		userMessages = []
		for message in messages:
			if message.author == member:
				userMessages.append(message)
		
		# owoify member's last non-command message
		if len(userMessages) > 0:
			for message in userMessages:
				if not isCommand(message.content):
					return self.owoify(message.content)
		
		return ""
	
	def owoify(self, words):
		return words.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
