"""
Note that Search arguments will be called with .lower() in commands.py, so there's no need to .lower() here
Categories: tags, artists, characters, parodies
"""

import requests
from re import search
from random import choice

from pasta.helpers.nsfw.hentai.sauce import Sauce
class Search:
	def __init__(self, category, info):
		self.info = info.replace(" ", "-")
		self.category = category.replace(" ", "-")
		self.url = "https://nhentai.net/{category}/{info}/popular".format(category=self.category, info=self.info)
		self.response = requests.get(self.url)
	
	def doesExist(self):
		return self.response.status_code != 404
	
	def getRandSauce(self):
		numbers = self.getNumbers()
		if len(numbers) > 0:
			# get a random sauce from numbers
			rand = choice(numbers)
			sauce = Sauce(rand)
			# do NOT submit loli or shota sauce
			while sauce.isIllegal():
				numbers.remove(rand)
				rand = choice(numbers)
				sauce = Sauce(rand)
			return sauce.getEmbed()
		return None
			
	def getNumbers(self):
		head = 	"<a href=\"/g/"
		tail = "/\" class=\"cover\""
		lines = self.getLines(head)
		numbers = []
		if len(lines) > 0:		
			for line in lines:
				# cool little solution to find in between head and tail
				number = line[line.find(head)+len(head):line.rfind(tail)]
				numbers.append(number)
		return numbers
	
	# looks for a head in a line of html
	def getLines(self, head):
		lines = []
		html = self.response.text
		for line in html.split('\n'):
			if head in line:
				lines.append(line)
		return lines