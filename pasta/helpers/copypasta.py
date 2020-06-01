"""
Class that sends a copypasta based on the last keyword in a lowercase discord message. There are some copypasta exceptions.
"""
import os
import discord
from re import split

from pasta.helpers.extrapasta import Extrapasta
from pasta.helpers.misc import getTriggers

class Copypasta:
	def __init__(self):
		self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
	
	async def fetch(self, message):
		# is it the navy seals copypasta?
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
		# an array of triggers. check for new content each time.
		TRIGGERS = getTriggers()
		# copypasta the last trigger word in the content
		reversedContent = reversed(split("[^a-z^A-Z^0-9]", content))
		for word in reversedContent:
			for trigger in TRIGGERS:
				if trigger in word:
					# sand exception
					#if trigger == "sand":
					return self.file2pasta(trigger).replace("{username}", message.author.mention)
				
		# if there's no copypasta, then return an empty string
		return ""
	
	def file2pasta(self, trigger):
		filename = "{this}/pastas/{trigger}.txt".format(this=self.THIS_FOLDER, trigger=trigger)
		file = open(filename, "r")
		text = file.read()
		file.close()
		return text