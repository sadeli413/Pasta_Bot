"""
# Title: Nhentai.py
# Author: Thad Shinno
# Description: class that returns an array of embeds given a lower case discord message. These embeds are nhentai links.
"""

# 227910 151529 177978 247896 283061  165961  177013  250401   301320  158990  151529  283061  247896  171461
# 227910 151529 177978 247896 283061  165961  177013  250401   301320  158990  171461

import discord
import requests

from re import split

class Nhentai:
	# global variable
	illegals = {}
	
	# return an array of embeds
	def getSauces(content):
		Nhentai.illegals = {}
		embeds = []
		if Nhentai.hasNumbers(content):
			numbers = Nhentai.getNumbers(content)
			# for every number in the content, make an embed
			for number in numbers:
				link = "https://nhentai.net/g/" + number
				response = requests.get(link)
				# don't make an embed if 404
				if response.status_code != 404:
					html = response.text
					print("fetching " + number)
					embed = Nhentai.getEmbed(html, link, number)
					if (embed.url is None):
						Nhentai.illegals[embed.title] = number
					embeds.append(embed)
		return embeds

	# an embed of Title, url, Artists, Numbers, Tags, and Parodies	
	def getEmbed(html, link, number):
		tags = Nhentai.getTags(html)
		embed = discord.Embed(
			title = Nhentai.getTitle(html),
			url = None if Nhentai.isIllegal(tags) else link
		)
		embed.set_author(name = "ARTISTS: " + Nhentai.getAuthors(html))
		embed.add_field(name = "SAUCE: ", value = number, inline=False)
		embed.add_field(name = "PAGES: ", value = Nhentai.getPages(html), inline=False)
		embed.add_field(name = "TAGS: ", value = tags, inline=False)
		# only attach parodies if they exist
		parodies = Nhentai.getParodies(html)
		if len(parodies) > 0:
			embed.add_field(name = "PARODIES: ", value = parodies, inline=False)
			
		return embed

	# return the title as a string. note that the title is found in the metadata
	def getTitle(html):
		# find the line with the title
		head = "<meta name=\"twitter:title\" content="
		line = Nhentai.getLine(html, head)
		line = line[len(head) + 2 : len(line) - 4]
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
	def getTags(html):
		# find the line with the tags
		head = "<meta name=\"twitter:description\" content="
		line = Nhentai.getLine(html, head)
		line = line[len(head) + 2 : len(line) - 4]
		
		tags = line.split(", ")
		return Nhentai.list2str(tags)
		
	# return the authors as a string. note that the authors are NOT found in the metadata	
	def getAuthors(html):
		head = "<span class=\"tags\"><a href=\"/artist/"
		line = Nhentai.getLine(html, head)
		# delete everything before >
		return Nhentai.getSpan(line)

	# return the authors as a string. note that the parodies are NOT found in the metadata
	def getParodies(html):
		head = "<span class=\"tags\"><a href=\"/parody/"
		line = Nhentai.getLine(html, head)
		# Return nothing if there are no parodies
		if len(line) < 1:
			return ""
		
		return Nhentai.getSpan(line)

	def getPages(html):
		tail = "pages</div>"
		line = Nhentai.getLine(html, tail)
		return line[9:-12]

	# return the data of a line as a string
	def getSpan(line):
		# split the line up from the html tags < and >
		words = split("[<>]", line)
		data = []
		# the necessary data is only found starting on the 4th index every 8 items
		for i in range(4, len(words), 8):
			word = words[i]
			data.append(word[:-1]) # append and remove a space

		# last item of parodies is always just an empty string
		data.pop()
		return Nhentai.list2str(data)
	
	# looks for a head in a line of html
	def getLine(html, head):
		for line in html.split('\n'):
			if head in line:
				return line
		return ""
	
	# gets valid numbers in lowercase content
	def getNumbers(content):
		# split up numbers in between special characters
		words = split("[^0-9]", content)
		
		# remove items that do not have numbers
		for word in reversed(words):
			if not Nhentai.hasNumbers(word):
				words.remove(word)

		# remove duplicates
		numbers = words
		numbers = list(dict.fromkeys(numbers))
		
		# numbers must be only five to seven digits
		for number in reversed(numbers):
			if len(number) < 5 or len(number) > 7:
				numbers.remove(number)
		
		return numbers
	
	
	def isIllegal(tags):
		return "loli" in tags or "shota" in tags
	
	
	def hasNumbers(word):
		return any(char.isdigit() for char in word)	
		
	# converts, a, list, into, a, string, like, this
	
	def list2str(list):
		out = ""
		for word in list:
			out += word + ", "
		
		return out[:-2]