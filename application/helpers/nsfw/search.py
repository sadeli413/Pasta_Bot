"""
Note that Search arguments will be called with .lower() in commands.py, so there's no need to .lower() here
Categories: tags, artists, characters, parodies
"""

import requests
# custom package
from application.helpers.nsfw.sauce import Sauce

class Search:
	def __init__(self, criteria):
		# search url
		self.criteria = criteria.replace(" ", "+").replace(":", "%3A" )
		self.url = "https://nhentai.net//api/galleries/search?query={criteria}&sort=popular".format(criteria=self.criteria)
		self.response = requests.get(self.url)
		self.data = self.response.json()
	
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
		
	# get all "numbers" on this page
	def getNumbers(self):
		numbers = []
		for key in self.data["result"]:
			numbers.append(str(key["id"]))
		return numbers