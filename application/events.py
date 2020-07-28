# @author Sadeli
"""
# Title: pasta_bot.py
# Author: Thad Shinno
# Description: contains on_message event. Encapsulate nhentai.py and copypasta.py
"""
import discord
from discord.ext import tasks, commands
from itertools import cycle
# custom packages
from application.helpers.misc import isCommand
from application.helpers.nsfw.nhentai import Nhentai
from application.helpers.copypasta import Copypasta

class Events:
	def __init__(self, client):
		self.client = client
		self.nh = Nhentai()
		self.cp = Copypasta()
	
	# send sauce or copypasta
	async def on_message(self, message):
		# ignore pasta_bot
		if message.author == self.client.user:
			return
		# don't pastafy or hentaify commands
		if not isCommand(message.content):
			"""		
			# NSFW works in DMChannels and nsfw channels
			doesNSFWWork = isinstance(message.channel, discord.DMChannel) or message.channel.is_nsfw()
			"""
			# if you don't find hentai, then send copypasta
			if not (await self.nh.fetch(message)):
				await self.cp.fetch(message)
				
		# let the bot process commands
		await self.client.process_commands(message)
	
	# get a cycle of pasta_bot statuses
	def getStatus(self):
		activities = [
			discord.Activity(name = ".help", type = discord.ActivityType.playing),
			discord.Activity(name = "lots of hentai.", type = discord.ActivityType.watching),
			discord.Activity(name = ".help", type = discord.ActivityType.playing),
			discord.Activity(name = "sad loli asmr.", type = discord.ActivityType.listening),
			discord.Activity(name = ".help", type = discord.ActivityType.playing),
			discord.Activity(name = "your local preschool.", type = discord.ActivityType.watching)
		]
		return cycle(activities)
		
		
		
		
