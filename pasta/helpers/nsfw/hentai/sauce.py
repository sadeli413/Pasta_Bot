"""
A single sauce has numbers, a webpage response, and the doujin info
"""

import discord
import requests
from re import split

class Sauce:
	def __init__(self, number):
		self.number = number
		self.response = requests.get("https://nhentai.net/g/" + self.number)
		self.dj = Doujin(number, self.response.text)
	
	def doesExist(self):
		return self.response.status_code == 200
	
	# an embed of Title, url, Artists, Sauce, Pages, Tags, and Parodies	
	def getEmbed(self):
		name = self.dj.getTitle()
		bad = self.isIllegal()
		embed = discord.Embed(
			title = "`{name}`".format(name=name) if len(name)>0 else "unreadable title",
			url = None if bad else self.dj.url,
			colour = discord.Colour.red() if bad else discord.Colour.blue()
		)
		# sauce-numbers, pages, and tags
		embed.add_field(name = "SAUCE: ", value = self.number, inline=False)
		embed.add_field(name = "PAGES: ", value = self.dj.getPages(), inline=False)
		embed.add_field(name = "TAGS: ", value = self.dj.getTags(), inline=False)
		# only atatch artists if they exist
		artists = self.dj.getArtists()
		if len(artists) > 0:
			embed.set_author(name = "ARTISTS: " + artists)
		# only attach parodies if they exist
		parodies = self.dj.getParodies()
		if len(parodies) > 0:
			embed.add_field(name = "PARODIES: ", value = parodies, inline=False)
			
		return embed
		
	def isIllegal(self):
		tags = self.dj.getTags()
		return "loli" in tags or "shota" in tags

class Doujin:
	def __init__(self, number, html):
		 self.number = number
		 self.html = html
		 self.url = "https://nhentai.net/g/" + self.number

	# return the title as a string. note that the title is found in the metadata
	def getTitle(self):
		# find the line with the title
		head = "<meta name=\"twitter:title\" content="
		line = self.getLine(head)
		line = line[len(head) + 2 : -4]
		# make sure the title is a printable character
		title = ""
		for char in line:
			if " " <= char and char <= "~":
				title += char
		# weird ascii codes
		title = title.replace("&#39;", "\'").replace("&quot;", "\"").replace("&lt;", "<").replace("&gt;", ">")
		
		return title

	# return the tags as a string. note that the tags are found in the metadata
	def getTags(self):
		# find the line with the tags
		head = "<meta name=\"twitter:description\" content="
		line = self.getLine(head)
		if len(line) > 0:	
			line = line[len(head) + 2 : -4]
			tags = line.split(", ")
			return self.list2str(tags)
		return ""
		
	# return the authors as a string. note that the authors are NOT found in the metadata	
	def getArtists(self):
		head = "<span class=\"tags\"><a href=\"/artist/"
		line = self.getLine(head)
		# delete everything before >
		return self.getSpan(line) if len(line) > 0 else ""
		# Return nothing if there are no artists

	# return the authors as a string. note that the parodies are NOT found in the metadata
	def getParodies(self):
		head = "<span class=\"tags\"><a href=\"/parody/"
		line = self.getLine(head)
		
		return self.getSpan(line) if len(line) > 0 else ""

	def getPages(self):
		tail = "pages</div>"
		line = self.getLine(tail)
		return line[9:-12] if len(line) > 0 else ""

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
	def getLine(self, head):
		for line in self.html.split('\n'):
			if head in line:
				return line
		return ""
		
	# "converts, a, list, into, a, string, like, this"
	def list2str(self, list):
		out = ""
		for word in list:
			out += word + ", "
		
		return out[:-2] # remove the last ", "