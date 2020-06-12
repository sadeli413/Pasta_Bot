"""
Note that Search arguments will be called with .lower() in commands.py, so there's no need to .lower() here
Categories: tags, artists, characters, parodies
"""

import requests
from random import choice
# custom package
from application.helpers.nsfw.hentai.sauce import Sauce

class Search:
	def __init__(self, criteria):
		# search url
		self.criteria = criteria.replace(" ", "+").replace(":", "%3A" )+ "+-loli+-shota"
		self.url = "https://nhentai.net/search/?q={criteria}&sort=popular".format(criteria=self.criteria)
		self.response = requests.get(self.url)
	
	def doesExist(self):
		return self.response.status_code == 200
	
	# maximum 25
	def getMultiSauce(self, amount):
		num = amount
		embeds = []
		numbers = self.getNumbers()
		if num > 0:
			# make sure num is not greater than len(numbers)
			if num > len(numbers):
				num = len(numbers)
			# get num amount of sauces
			if len(numbers) > 0:
				for i in range(num):
					embeds.append(Sauce(numbers[i]).getEmbed())
		return embeds
		
	def getRandSauce(self, amount):
		num = amount
		embeds = []
		numbers = self.getNumbers()
		if num > 0:
			# make sure num is not greater than len(numbers)
			if num > len(numbers):
				num = len(numbers)
			# get random sauces: limit is len(numbers) and num amount
			i = 0
			while len(numbers) > 0 and i < num:
				print("fetching...")
				# get a random sauce from numbers
				rand = choice(numbers)
				sauce = Sauce(rand)
				# do NOT submit loli or shota sauce
				while sauce.isIllegal():
					numbers.remove(rand)
					rand = choice(numbers)
					sauce = Sauce(rand)
				embeds.append(sauce.getEmbed())
				# make sure there are no duplicates
				numbers.remove(rand)
				i += 1
		return embeds
		
	# get all "numbers" on this page
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
