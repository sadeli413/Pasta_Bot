"""
# Title: pasta_bot.py
# Author: Thad Shinno
# Description: contains on_message event. Encapsulate nhentai.py and copypasta.py
"""
import discord

from discord.ext import tasks, commands
from itertools import cycle
from pasta.misc import isCommand
from .eventHelpers.nhentai import Nhentai
from .eventHelpers.copypasta import Copypasta

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
			# if sauce isn't found, then send copypasta
			if not await self.nh.fetch(message):
				await self.cp.fetch(message)
		
		# let the bot process commands
		await self.client.process_commands(message)
	
	# get a cycle of pasta_bot statuses
	def getStatus(self):
		activities = []
		activities.append(discord.Activity(name = "lots of hentai.", type = discord.ActivityType.watching))
		activities.append(discord.Activity(name = "sad loli asmr.", type = discord.ActivityType.listening))
		return cycle(activities)