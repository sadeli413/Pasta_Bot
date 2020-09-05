# @author Sadeli
"""
Note that Search arguments will be called with .lower() in commands.py, so there's no need to .lower() here
Categories: tags, artists, characters, parodies
"""

import requests
from re import sub, search
from random import randint, choice
# custom package
from application.helpers.nsfw.sauce import Sauce

class Search:
	def __init__(self, criteria):
		# search url
		self.criteria = criteria
		self.AQ = self.amountAndQuery()
		if len(self.AQ) > 0:
			self.url = "https://nhentai.net//api/galleries/search?query={query}&sort=popular".format(query=self.AQ["query"])
			self.response = requests.get(self.url)
			if self.doesExist():
				self.data = self.response.json()
			else:
				self.data = None
	
	def doesExist(self):
		return self.response.status_code == 200
	
	# get amount sauce of a search criteria
	async def withArgs(self, ctx, flag):
		if flag == "random":
			embeds = self.getRandSauce(self.getNumbers()) # get amount number of numbers given by criteria
		else:
			embeds = self.getMultiSauce()
		# make sure the embed will be valid
		if len(embeds) > 0:
			for embed in embeds:
				await ctx.send(embed=embed)
		else:
			await ctx.send("Could not find {userquery}".format(userquery=self.AQ["userquery"]))

	# maximum 25
	def getMultiSauce(self):
		amount = self.AQ["amount"]
		embeds = []
		numbers = self.getNumbers()
		if amount > 0:
			# make sure namount um is not greater than len(numbers)
			if amount > len(numbers):
				amount = len(numbers)
			# get num amount of sauces
			if len(numbers) > 0:
				for i in range(amount):
					print(numbers[i], end = " ")
					embeds.append(Sauce(numbers[i]).getEmbed())
				print()
		return embeds

	def getRandSauce(self, numbers):
		amount = self.AQ["amount"]
		embeds = []
		if amount > 0:
			# make sure num is not greater than how many numbers there are
			if amount > len(numbers):
				amount = len(numbers)
			# get random sauces: limit is len(numbers) and num amount
			i = 0
			while len(numbers) > 0 and i < amount:
				# get a random sauce from numbers
				rand = choice(numbers)
				print(rand, end = " ")
				sauce = Sauce(rand)
				embeds.append(sauce.getEmbed())
				# make sure there are no duplicates
				numbers.remove(rand)
				i += 1
			print()
		return embeds
		
	# get all "numbers" on the search page
	def getNumbers(self):
		numbers = []
		if self.data is not None:
			for key in self.data["result"]:
				numbers.append(str(key["id"])) # id is something like 177013
		return numbers

	# [amount] {query}
	def amountAndQuery(self):
		#sanitize query
		sanitized = self.sanitize(self.criteria)
		if not search("[A-Za-z0-9]", sanitized):
			return {}

		query = sanitized
		# get amount
		args = query.split(" ")
		first = args[0]
		# if there's only a number search that or if there's no number, amount is 1
		if query.isnumeric() or not first.isnumeric():
			amount = 1
		else:
			# set amount and remove the amount from query
			amount = abs(int(first))
			args.pop(0)
			query = "".join(i + " " for i in args)[:-1] # delete the final space
			# url sanitizer
			# query = query.replace(" ", "+").replace(":", "%3A" )
		return {
			"sanitized": sanitized,
			"amount": amount,
			"query": query.replace(" ", "+").replace(":", "%3A" ),
			"userquery": query
		}

	# remove multiple whitespace and special characters besides :"\s
	def sanitize(self, word):
		new = word.lower()
		new = sub("\s+", " ", new)
		new = sub(":+", ":", new)
		new = sub("\"+", "\"", new)
		new = sub("-+", "-", new)
		new = sub("[^A-Za-z0-9\-:\"\s]", "", new)
		new = new.strip()
		return new

	# get one random sauce
	@staticmethod
	async def noArgs(ctx):
		rand = randint(10000, 999999)
		print(rand, end = " ")
		sauce = Sauce(str(rand))
		# make sure it exists
		while (not sauce.doesExist()):
			print(rand, end = " ")
			rand = randint(10000, 999999)
			sauce = Sauce(str(rand))
		
		print("GAVE: " + sauce.number)
		await ctx.send(embed=sauce.getEmbed())

	