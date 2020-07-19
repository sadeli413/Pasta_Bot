"""
Commands: help, ignore, readme, owo, shutdown, clean, triggers, random, search
"""
import discord
import os
import requests
from re import sub, search
# custom packages
from application.helpers.misc import getTriggers, isCommand
from application.helpers.owo import Owo
from application.helpers.nsfw.randomSearch import randomSearch
from application.helpers.nsfw.search import Search
from application.helpers.extrapasta import Extrapasta
from application.helpers.help import Help

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
			arg = self.alias(arg)
			await ctx.author.send(embed = self.hp.botDictionary[arg].embed)
		await ctx.send("{author} I sent you a DM".format(author=ctx.author.mention))
	
	def alias(self, arg):
		if arg == ".i":
			return ".ignore"
		elif arg == ".h":
			return ".help"
		elif arg == ".trigger":
			return ".triggers"
		elif arg == ".uwu":
			return ".owo"
		else:
			return arg
	
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
	# does NOT send minors
	async def search(self, ctx, criteria):
		"""
		# search only works in DMChannels and NSFW channels
		if (not isinstance(ctx.channel, discord.DMChannel)):
			if not ctx.channel.is_nsfw():
				await ctx.send("```css\n.search only works in nsfw channels```")
				return
		"""
		# remove special characters
		info = criteria.lower()
		info = self.sanitize(info)
		if len(info) < 1 or not search("[A-Za-z0-9]", info):
			await ctx.send("```css\n.search [amount] {search criteria}\nGet some .help```")
			return
	
		aAndC = self.amountAndCriteria(info)
		amount = aAndC["amount"]
		info = aAndC["criteria"]
		# search the criteria
		if amount > 0:
			# kinkshame if searched for lolis
			if self.isKinkshame(ctx, info):
				await ctx.send(Extrapasta.fbiOpenUp())
				return
			
			await ctx.send("Searching{amount} for `{info}`...".format(amount = " x" + str(amount) if amount > 1 else "", info=info))
			# send search normally
			find = Search(info)
			embeds = find.getMultiSauce(amount)
			if len(embeds) > 0:
				for embed in embeds:
					await ctx.send(embed=embed)
			else:
				await ctx.send("Found no `{info}` ||Or it's all loli/shota||".format(info=info))
	
	# searches top 25 most popular and gives a random one, or an amount
	async def random(self, ctx, criteria):
		"""
		# only works in DMChannels and NSFW channels
		if (not isinstance(ctx.channel, discord.DMChannel)):
			if not ctx.channel.is_nsfw():
				await ctx.send("```css\n.random only works in nsfw channels```")
				return
		"""	
		rs = randomSearch()
		# no arguments
		if len(criteria) < 1:
			await ctx.send("Fetching random sauce...")
			await rs.noArgs(ctx)
			print("done")
			return
		
		# remove special characters
		info = criteria.lower()
		info = self.sanitize(info)
		if not search("[A-Za-z0-9]", info):
			await ctx.send("```css\n.random [amount] [search criteria]\nGet some .help```")
			return
		
		# a single number argument
		if info.strip().isnumeric():
			amount = abs(int(info))
			if amount > 0:
				await ctx.send("Fetching random sauce{amount}...".format(amount=" x"+str(amount) if amount > 1 else ""))
				for i in range(amount):
					await rs.noArgs(ctx)
				print("done")
		
		# [amount] {criteria} args
		else:
			aAndC = self.amountAndCriteria(info)
			amount = aAndC["amount"]
			info = aAndC["criteria"]
			
			if amount > 0:
				# kink shame if searched for minors
				if self.isKinkshame(ctx, info):
					await ctx.send(Extrapasta.fbiOpenUp())
					return
						
				await ctx.send("Random search{amount}{extra}...".format(amount=" x" + str(amount) if amount > 1 else "", extra =" for `" + info + "`" if len(info) > 0 else ""))
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


	"""
	The rest are helper funcitons
	"""
	# of the past 200 messages, delete those sent by Pasta_Bot
	async def clean(self, ctx):
		deleted = await ctx.channel.purge(limit = 200, check=self.isBot)
		await ctx.send('Deleted {num} Pasta_Bot message(s)'.format(num = len(deleted)))
	
	def isBot(self, message):
		return message.author == self.client.user
	
	# info is already lowered and sanitized
	def amountAndCriteria(self, info):
		# get amount
		crit = info.strip()
		args = crit.split(" ")
		first = args[0]
		# if there's only a number search that or If there's no number, amount is 1
		if crit.isnumeric() or not first.isnumeric():
			amount = 1
		# set amount, and remove it from info
		else:
			amount = abs(int(first))
			args.pop(0)
			crit = "".join(i + " " for i in args)[:-1] # delete the space at the end
		return {
			"amount":amount,
			"criteria":crit
		}
	
	def isKinkshame(self, ctx, info):
		for arg in info.split(" "):
			if ("loli" in arg or "shota" in arg) and not arg[0].startswith("-"):
				return True
		return False
		
	# remove multiple whitespace and special characters besides :"\s
	def sanitize(self, word):
		new = sub("\s+", " ", word)
		new = sub(":+", ":", new)
		new = sub("\"+", "\"", new)
		new = sub("-+", "-", new)
		new = sub("[^A-Z^a-z^0-9^\-^:^\"^\s]", "", new)
		return new
