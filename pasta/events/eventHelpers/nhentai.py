"""
# Title: Nhentai.py
# Author: Thad Shinno
# Description: Fetches nhentai links
"""
"""
Test cases
227910 151529 177978 247896 283061  165961  177013  250401   301320  158990  151529  283061  247896  171461
227910 151529 177978 247896 283061  165961  177013  250401   301320  158990  171461
"""
import discord
import requests

from re import split
from .extrapasta import Extrapasta

class Nhentai:
	# illegals is a dictionary containing title:sauce_number
	def __init__(self):
		self.illegals = {}
	
	async def fetch(self, message):
		content = message.content.lower()
		sauces = self.getSauces(content)
		if len(sauces) > 0:
			# if there's more than 3, then tell them thats a lot
			if len(sauces) > 3:
				await message.channel.send(Extrapasta.tooMuchHentai())
			# give all the sauce
			for sauce in sauces:
				await message.channel.send(embed = sauce)
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
	def getSauces(self, content):
		self.illegals = {}
		embeds = []
		if self.hasNumbers(content):
			numbers = self.getNumbers(content)
			# for every number in the content, make an embed
			for number in numbers:
				link = "https://nhentai.net/g/" + number
				response = requests.get(link)
				# don't make an embed if 404
				if response.status_code != 404:
					html = response.text
					print("fetching " + number)
					embed = self.getEmbed(html, link, number)
					if (embed.url is None):
						self.illegals[embed.title] = number
					embeds.append(embed)
		return embeds

	# an embed of Title, url, Artists, Sauce, Pages, Tags, and Parodies	
	def getEmbed(self, html, link, number):
		tags = self.getTags(html)
		embed = discord.Embed(
			title = self.getTitle(html),
			url = None if self.isIllegal(tags) else link
		)
		embed.set_author(name = "ARTISTS: " + self.getAuthors(html))
		embed.add_field(name = "SAUCE: ", value = number, inline=False)
		embed.add_field(name = "PAGES: ", value = self.getPages(html), inline=False)
		embed.add_field(name = "TAGS: ", value = tags, inline=False)
		# only attach parodies if they exist
		parodies = self.getParodies(html)
		if len(parodies) > 0:
			embed.add_field(name = "PARODIES: ", value = parodies, inline=False)
			
		return embed

	# return the title as a string. note that the title is found in the metadata
	def getTitle(self, html):
		# find the line with the title
		head = "<meta name=\"twitter:title\" content="
		line = self.getLine(html, head)
		line = line[len(head) + 2 : -4]
		# make sure the title is a printable character
		title = ""
		for char in line:
			if " " <= char and char <= "~":
				title += char
		# weird ascii code for apostrophe 
		apostrophe = "&#39;"
		title = title.replace("&#39;", "\'")
		
		return title

	# return the tags as a string. note that the tags are found in the metadata
	def getTags(self, html):
		# find the line with the tags
		head = "<meta name=\"twitter:description\" content="
		line = self.getLine(html, head)
		line = line[len(head) + 2 : -4]
		
		tags = line.split(", ")
		return self.list2str(tags)
		
	# return the authors as a string. note that the authors are NOT found in the metadata	
	def getAuthors(self, html):
		head = "<span class=\"tags\"><a href=\"/artist/"
		line = self.getLine(html, head)
		# delete everything before >
		return self.getSpan(line)

	# return the authors as a string. note that the parodies are NOT found in the metadata
	def getParodies(self, html):
		head = "<span class=\"tags\"><a href=\"/parody/"
		line = self.getLine(html, head)
		if len(line) > 0:
			return self.getSpan(line)
		
		# Return nothing if there are no parodies
		return ""

	def getPages(self, html):
		tail = "pages</div>"
		line = self.getLine(html, tail)
		return line[9:-12]

	# return the data of a line as a string
	def getSpan(self, line):
		# split the line up from the html tags < and >
		words = split("[<>]", line)
		data = []
		# the necessary data is only found starting on the 4th index every 8 items
		for i in range(4, len(words), 8):
			data.append(words[i][:-1]) # append and remove a space

		# last item of parodies is always just an empty string
		data.pop()
		return self.list2str(data)
	
	# looks for a head in a line of html
	def getLine(self, html, head):
		for line in html.split('\n'):
			if head in line:
				return line
		return ""
	
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
	
	def isIllegal(self, tags):
		return "loli" in tags or "shota" in tags
	
	def hasNumbers(self, word):
		return any(char.isdigit() for char in word)	
		
	# "converts, a, list, into, a, string, like, this"
	def list2str(self, list):
		out = ""
		for word in list:
			out += word + ", "
		
		return out[:-2]