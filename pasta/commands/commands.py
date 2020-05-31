"""
# Title: pasta_bot.py
# Author: Thad Shinno
# Description: readme, triggers, owo, clean commands
"""

import discord
import os
from pasta.misc import getTriggers, isCommand

class Commands:
	def __init__(self, client):
		self.client = client
		self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
	
	# DM README.txt
	async def readme(self, ctx):
		await ctx.author.send("Description of Pasta_Bot", file=discord.File(self.THIS_FOLDER + "../../README.txt"))
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# DM a list of triggers
	async def triggers(self, ctx):
		triggerList = getTriggers()
		triggers = "These are the following trigger words:\n"
		for i in range(len(triggerList)):
			triggers += "{num}) {trigger}\n".format(num=i+1, trigger=triggerList[i])
		await ctx.author.send(triggers)
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# owoify member messages
	async def owo(self, ctx, *members : discord.Member):
		# if no members are given, then just owoify last valid message
		if len(members) < 1:
			allMessages = await ctx.channel.history(limit=20).flatten()
			for message in allMessages:
				# owoify the first non-command
				if not isCommand(message.content):
					owoify = self.owoify(message.content)
					if len(owoify) > 0:
						return await ctx.send(owoify)
		else:
			# else if members are given, then owoify last messages only from those members
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
	
	async def clean(self, ctx):
		deleted = await ctx.channel.purge(limit = 200, check=self.isBot)
		await ctx.send('Deleted {num} message(s)'.format(num = len(deleted)))
	
	def isBot(self, message):
		return message.author == self.client.user
	
	def owoify(self, words):
		return words.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")