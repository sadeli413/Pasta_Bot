"""
Fetch Nhentai links

"Test cases"
185217 301659 165961 262340 250750 298547 287158 235879
151529 161727 158990
276728 280751
80759 104248
255768 274826
278041 226081 267270 220309 237868

edge debugging cases:
176234 152246 284672 612568 315105
"""
import discord
import requests
from re import split
#custom packages
from pasta.helpers.extrapasta import Extrapasta
from pasta.helpers.nsfw.hentai.sauce import Sauce

class Nhentai:
	# keep track of number of illegals
	def __init__(self):
		self.illegals = 0
	
	async def fetch(self, message):
		sauces = await self.getSauces(message)
		if len(sauces) > 0:
			# if there's more than 3, then tell them thats a lot
			if len(sauces) > 3:
				await message.channel.send(Extrapasta.tooMuchHentai())
			# give all the sauce
			for sauce in sauces:
				await message.channel.send(embed=sauce)
			# notify if there are loli or shota tags
			if self.illegals > 0:
				await message.channel.send(Extrapasta.fbiOpenUp())
			print("done")
			# sauce was found
			return True
		# no sauce
		return False
	
	# return an array of embeds
	async def getSauces(self, message):
		content = message.content.lower()
		self.illegals = 0
		embeds = []
		#if self.hasNumbers(content):
		numbers = self.getNumbers(content)
		if len(numbers) > 0:
			# for every number in the content, make an embed
			await message.channel.send("Fetching sauce...")
			for number in numbers:
				sauce = Sauce(number)
				if sauce.doesExist():
					print("fetching...")
					embeds.append(sauce.getEmbed())
					if sauce.isIllegal():
						self.illegals += 1
				else:
					await message.channel.send("||{number} is invalid sauce (404).||".format(number=number))
		return embeds
			
	# gets valid numbers in lowercase content
	def getNumbers(self, content):
		if not self.hasNumbers(content):
			return []
			
		# split up numbers in between special characters
		words = split("[^0-9]", content)
		# remove items that do not have numbers or arent five/six digits
		for word in reversed(words):
			isBadLength = len(word) < 5 or len(word) > 6
			if (not self.hasNumbers(word)) or isBadLength:
				words.remove(word)
		# remove duplicates
		numbers = list(dict.fromkeys(words))
		"""
		# numbers must be only five to seven digits
		for number in reversed(numbers):
			if len(number) < 5 or len(number) > 7:
				numbers.remove(number)
		"""
		return numbers
				
	def hasNumbers(self, word):
		return any(char.isdigit() for char in word)	