# @author Sadeli
"""
Commands: help, ignore, owo, shutdown, clean, triggers, random, search
"""
import discord
import os
import requests
import datetime
from re import sub, search
# custom packages
import application.helpers.owo as Owoifier
import application.helpers.extrapasta as Extrapasta
from application.helpers.misc import getTriggers, isCommand, timestamp
from application.helpers.nsfw.search import Search
from application.helpers.help import Help

class Commands:
	def __init__(self, client):
		self.client = client
		self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		# self.owoifier = Owo()
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
			await ctx.send("{author}, I sent you a DM".format(author=ctx.author.name))
		else:
			# transform aliases
			arg = self.alias(arg)
			await ctx.send(embed = self.hp.botDictionary[arg].embed)
			
	# command aliases
	def alias(self, arg):
		aliases = {
			".i": ".ignore",
			".h": ".help",
			".trigger": ".triggers",
			".uwu": ".owo"
		}
		return aliases.get(arg, arg)
	
	# DM a list of triggers
	async def triggers(self, ctx):
		# create trigger message
		triggerList = getTriggers()
		triggers = "```bash\nThese are the working trigger words\n"
		for i in range(len(triggerList)):
			triggers += "{num}) \"{trigger}\"\n".format(num=i+1, trigger=triggerList[i])
		triggers += "```"
		# send DM notice to channel and DM the trigger message 
		await ctx.author.send(triggers)
		await ctx.send("{member} I sent you a DM".format(member=ctx.author.mention))
	
	# .search [amount] {criteria}
	# does NOT send minors
	async def search(self, ctx, criteria):
		print(ctx.message.content, end = " ... ")
	
		# remove special characters
		find = Search(criteria)
		aq = find.AQ
		if len(aq) < 1:
			await ctx.send("```css\n.search [amount] {search criteria}\nGet some .help```")
			return

		# search the criteria
		if aq["amount"] > 0:
			# kinkshame if searched for lolis
			if self.isKinkshame(ctx, aq["query"]):
				await ctx.send(Extrapasta.fbiOpenUp())
				return
			
			await ctx.send("Searching{amount} for `{query}`...".format(amount = " x" + str(aq["amount"]) if aq["amount"] > 1 else "", query=aq["query"]))
			await find.withArgs(ctx, "notrandom")
			
			timestamp()
	
	# searches top 25 most popular and gives a random one, or an amount
	async def random(self, ctx, criteria):
		print(ctx.message.content, end = " ... ")
	
		# no arguments
		if len(criteria) < 1:
			await ctx.send("Fetching random sauce...")
			await Search.noArgs(ctx)
			timestamp()
			return
		
		# remove special characters
		find = Search(criteria)
		aq = find.AQ
		if len(aq) < 1:
			await ctx.send("```css\n.random [amount] [search criteria]\nGet some .help```")
			return
		
		# a single number argument
		if aq["sanitized"].isnumeric():
			amount = abs(int(aq["sanitized"]))
			if amount > 0:
				await ctx.send("Fetching random sauce{amount}...".format(amount=" x"+str(amount) if amount > 1 else ""))
				for i in range(amount):
					await Search.noArgs(ctx)

		else:
			# [amount] [criteria] args
			if aq["amount"] > 0:
				# kink shame if searched for minors
				if self.isKinkshame(ctx, aq["query"]):
					await ctx.send(Extrapasta.fbiOpenUp())
					return
						
				await ctx.send("Random search{amount}{query}...".format(amount=" x" + str(aq["amount"]) if aq["amount"] > 1 else "", query =" for `" + aq["query"] + "`" if len(aq["query"]) > 0 else ""))
				await find.withArgs(ctx, "random")
		timestamp()

	# check if the user searched for loli or shota
	def isKinkshame(self, ctx, info):
		# ensure that removal tags like -tag:loli does NOT get kinkshamed
		for arg in info.split(" "):
			if ("loli" in arg or "shota" in arg) and not arg[0].startswith("-"):
				return True
		return False
					
	# owoify member messages
	async def owo(self, ctx, *members : discord.Member):
		# if no members are given, then just owoify last valid message
		if len(members) < 1:
			await Owoifier.noMember(ctx)
		# if there are members, then owoify just their messages
		else:
			await Owoifier.yesMember(ctx, *members)

	# send a broadcast message to all servers
	async def broadcast(self, channel, announcement):
		if len(announcement) > 0:
			await channel.send(announcement)
				
	async def giveError(self, ctx, error, OWNER):
		print()
		print("******")
		print(error)
		timestamp()
		print("******")
		print()
		message = "uwu I'm sorry senpai... something has gone terribly wrong\n"
		message += "Pwease contact Sadeli to fix a possible bug"
		await ctx.send(message)
		# send message to owner
		if isinstance(ctx.channel, discord.DMChannel):
			guild = ctx.author.name + "'s DM channel."
			channel = ""
		else:
			guild = ctx.message.guild.name
			channel = ctx.channel.name
		err = "An error has occured at Guild **{guild}** in Channel **{channel}** from:```css\n{message}```"
		await OWNER.send(err.format(guild=guild, channel=channel, message=ctx.message.content))

	# of the past 200 messages, delete those sent by Pasta_Bot
	async def clean(self, ctx):
		deleted = await ctx.channel.purge(limit = 200, check=self.isBot)
		await ctx.send('Deleted {num} Pasta_Bot message(s)'.format(num = len(deleted)))
	
	def isBot(self, message):
		return message.author == self.client.user