# @author Sadeli
"""
Class that sends a copypasta based on the last keyword in a lowercase discord message. There are some copypasta exceptions.
"""
import os
import discord
from re import split

from application.helpers.extrapasta import Extrapasta
from application.helpers.misc import getTriggers

class Copypasta:
	def __init__(self):
		self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
	
	async def fetch(self, message):
		# is the message the navy seals copypasta?
		response = Extrapasta.sealResponse(message.content.lower())
		if len(response) > 0:
			await message.channel.send(response)
		# otherwise, respond to pasta normally
		else:
			pasta = self.getPasta(message)
			if len(pasta) > 0:
				await message.channel.send(pasta)
	
	# return a string copypasta based on a full message content
	def getPasta(self, message):
		content = message.content.lower()
		TRIGGERS = getTriggers() # you can actually edit the triggers while the bot is running
		# copypasta the last trigger word in the content
		reversedContent = reversed(split("[^a-z^A-Z^0-9]", content))
		for word in reversedContent:
			for trigger in TRIGGERS:
				if trigger in word:
					return self.file2pasta(trigger).replace("{username}", message.author.mention)
				
		# if there's no copypasta, then return an empty string
		return ""
	
	# return the copypasta from a file
	def file2pasta(self, trigger):
		# get the file
		try:
			filename = "{this}/pastas/{trigger}.txt".format(this=self.THIS_FOLDER, trigger=trigger)
			file = open(filename, "r")
			# read and return text
			text = file.read()
			file.close()
			return text
		except:
			print("could not open copypasta file")
			exit(1)
