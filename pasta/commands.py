"""
Commands: readme, triggers, owo, clean, and surprise commands
"""

import discord
import os
import requests
from random import randint

# custom packages
from pasta.helpers.misc import getTriggers
from pasta.helpers.owo import Owo
from pasta.helpers.nsfwl.randomSearch import randomSearch

class Commands:
	def __init__(self, client):
		self.client = client
		self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		self.owoifier = Owo()
	
	# DM README.txt
	async def readme(self, ctx):
		await ctx.author.send("Description of Pasta_Bot", file=discord.File(self.THIS_FOLDER + "../../README.txt"))
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# DM a list of triggers
	async def triggers(self, ctx):
		triggerList = getTriggers()
		triggers = "These are the working trigger words:\n"
		for i in range(len(triggerList)):
			triggers += "{num}) {trigger}\n".format(num=i+1, trigger=triggerList[i])
		await ctx.author.send(triggers)
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# searches top 25 most popular and gives a random one
	async def random(self, ctx, data):
		rs = randomSearch()
		if len(data) < 1:
			await rs.noArgs(ctx)
		elif len(data) > 1:
			await rs.yesArgs(ctx, data)
		else:
			raise discord.ext.commands.BadArgument()
	
	# owoify member messages
	async def owo(self, ctx, *members : discord.Member):
		# if no members are given, then just owoify last valid message
		if len(members) < 1:
			await self.owoifier.noMember(ctx)
		# if there are members, then owoify just their messages
		else:
			await self.owoifier.yesMember(ctx, *members)

	# of the past 200 messages, delete those sent by Pasta_Bot
	async def clean(self, ctx):
		deleted = await ctx.channel.purge(limit = 200, check=self.isBot)
		await ctx.send('Deleted {num} Pasta_Bot message(s)'.format(num = len(deleted)))
	
	def isBot(self, message):
		return message.author == self.client.user