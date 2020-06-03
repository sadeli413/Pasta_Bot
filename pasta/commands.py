"""
Commands: help, ignore, readme, owo, shutdown, clean, triggers, random, search
"""

import discord
import os
import requests
from re import sub, search
from random import randint

# custom packages
from pasta.helpers.misc import getTriggers
from pasta.helpers.misc import isCommand
from pasta.helpers.owo import Owo
from pasta.helpers.nsfw.randomSearch import randomSearch
from pasta.helpers.nsfw.search import Search
from pasta.helpers.extrapasta import Extrapasta
from pasta.helpers.help import Help

class Commands:
	def __init__(self, client):
		self.client = client
		self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		self.owoifier = Owo()
		self.hp = Help()
	
	# send help
	async def help(self, ctx, spec):
		arg = spec.lower()
		# make argument starts with "."
		if not arg.startswith("."):
			arg = "." + arg
		# if there's no argument or no real command	
		if len(spec) < 1 or not isCommand(arg):
			await ctx.author.send(self.hp.msg)
		else:
			# transform aliases
			if arg == ".i":
				arg = ".ignore"
			elif arg == ".h":
				arg = ".help"
			elif arg == ".trigger":
				arg = ".triggers"
			elif arg == ".uwu":
				arg = ".owo"
			await ctx.author.send(embed = self.hp.botDictionary[arg].embed)
		await ctx.send("{author} I sent you a DM".format(author=ctx.author.mention))
	
	# DM README.txt
	async def readme(self, ctx):
		await ctx.author.send("`Description of Pasta_Bot`", file=discord.File(self.THIS_FOLDER + "../../README.txt"))
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# DM a list of triggers
	async def triggers(self, ctx):
		triggerList = getTriggers()
		triggers = "```bash\nThese are the working trigger words\n"
		for i in range(len(triggerList)):
			triggers += "{num}) \"{trigger}\"\n".format(num=i+1, trigger=triggerList[i])
		triggers += "```"
		await ctx.author.send(triggers)
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# .search [amount] {criteria}
	async def search(self, ctx, criteria):
		# get amount
		info = criteria.lower()
		info = sub("[^A-Z^a-z^0-9^:^\"]", "", info)
		if len(info) < 1 or not search("[A-Za-z0-9]", info):
			raise Exception()				
		args = info.split(" ")
		first = args[0]
		# if there's only a number search that or If there's no number, amount is 1
		if criteria.isnumeric() or not first.isnumeric():
			amount = 1
		# # set amount, and remove it from info
		else:
			amount = abs(int(first))
			args.pop(0)
			info = "".join(i + " " for i in args)[:-1] # delete the space at the end
		
		# search the criteria
		await ctx.send("Searching for `{info}`...".format(info=info))
		# kinkshame if searched for lolis
		for arg in args:
				if ("loli" in arg or "shota" in arg) and arg[0] != "-":
					await ctx.send(Extrapasta.fbiOpenUp())
		find = Search(info)
		embeds = find.getMultiSauce(amount)
		if len(embeds) > 0:
			for embed in embeds:
				await ctx.send(embed=embed)
		else:
			await("Found no `{info}`".format(info=info))
	
	# searches top 25 most popular and gives a random one, or an amount
	async def random(self, ctx, criteria):
		rs = randomSearch()
		# no arguments
		if len(criteria) < 1:
			await ctx.send("Fetching random sauce...")
			await rs.noArgs(ctx)
			print("done")
		# a single number argument
		elif criteria.isnumeric():
			amount = abs(int(criteria))
			if amount > 0:
				await ctx.send("Fetching random sauce{amount}...".format(amount=" x"+str(amount) if amount > 1 else ""))
				for i in range(amount):
					await rs.noArgs(ctx)
				print("done")
		# [amount] {criteria} args
		else:
			# check for amount
			info = criteria.lower()
			info = sub("[^A-Z^a-z^0-9^:^\"]", "", info)
			if not search("[A-Za-z0-9]", info):
				raise Exception()
			args = info.split(" ")
			first = args[0]
			if first.isnumeric():
				# set amount, and remove it from info
				amount = abs(int(first))
				args.pop(0)
				info = "".join(i + " " for i in args)[:-1] # delete the last space
			# if there's no amount, then set default 1
			else:
				amount = 1
				
			await ctx.send("Random search{amount} for `{info}`...".format(amount=" x" + str(amount) if amount > 1 else "", info=info))
			# kink shame if searched for minors
			for arg in args:
				if ("loli" in arg or "shota" in arg) and arg[0] != "-":
					await ctx.send(Extrapasta.fbiOpenUp())
			await rs.yesArgs(ctx, amount, info)
			print("done")
					
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