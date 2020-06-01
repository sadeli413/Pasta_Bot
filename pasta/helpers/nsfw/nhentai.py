"""
# Title: Nhentai.py
# Author: Thad Shinno
# Description: Fetches nhentai links
"""
"""
Test cases
176234 151529 158990 185217 152246 284672 301659 165961 612568
"""
import discord
import requests

from re import split
from pasta.helpers.extrapasta import Extrapasta
from pasta.helpers.nsfw.sauce import Sauce

class Nhentai:
	# illegals is a dictionary containing title:sauce_number
	def __init__(self):
		self.illegals = {}
	
	async def fetch(self, message):
		# content = message.content.lower()
		sauces = await self.getSauces(message)
		if len(sauces) > 0:
			# if there's more than 3, then tell them thats a lot
			if len(sauces) > 3:
				await message.channel.send(Extrapasta.tooMuchHentai())
			# give all the sauce
			for sauce in sauces:
				await message.channel.send(embed=sauce)
			# notify if there are loli or shota tags
			if len(self.illegals) > 0:
				fbi = Extrapasta.fbiOpenUp() + "\n"
				for title in self.illegals:
					fbi += "- *{title}*  ({numbers})\n".format(title=title, numbers = self.illegals.get(title))
				await message.channel.send(fbi)
			print("done fetching")
			# sauce was found
			return True
		# no sauce
		return False
	
	# return an array of embeds
	async def getSauces(self, message):
		content = message.content.lower()
		self.illegals = {}
		embeds = []
		if self.hasNumbers(content):
			numbers = self.getNumbers(content)
			# for every number in the content, make an embed
			for number in numbers:
				sauce = Sauce(number)
				if sauce.doesExist():
					print("fetching " + number)
					embeds.append(sauce.getEmbed())
					if sauce.isIllegal():
						self.illegals[sauce.dj.getTitle()] = number
				else:
					await message.channel.send("{number} is invalid sauce.".format(number=number))
		
		return embeds
			
	# gets valid numbers in lowercase content
	def getNumbers(self, content):
		# split up numbers in between special characters
		words = split("[^0-9]", content)
		# remove items that do not have numbers
		for word in reversed(words):
			if not self.hasNumbers(word):
				words.remove(word)
		# remove duplicates
		numbers = list(dict.fromkeys(words))
		# numbers must be only five to seven digits
		for number in reversed(numbers):
			if len(number) < 5 or len(number) > 7:
				numbers.remove(number)
		
		return numbers
				
	def hasNumbers(self, word):
		return any(char.isdigit() for char in word)	