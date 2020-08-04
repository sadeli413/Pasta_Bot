# @author Sadeli
"""
Randomly searches for a doujin. does NOT grab doujins with "loli" or "shota" in the tags
"""
import discord
from random import randint
from random import choice
# custom packages
from application.helpers.nsfw.sauce import Sauce
from application.helpers.nsfw.search import Search

class randomSearch:
	def __init__(self):
		pass
	
	# get one random sauce
	async def noArgs(self, ctx):
		
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
	
	# get amount sauce of a search criteria
	async def yesArgs(self, ctx, amount, criteria):
		# print(ctx.message.content, end = " ")
		find = Search(criteria)	# get criteria search query
		if not find.doesExist():
			await ctx.send("Found no `{criteria}`".format(criteria=criteria))
			return
		embeds = self.getRandSauce(amount, find.getNumbers()) # get amount number of numbers given by criteria
		# make sure the embed will be valid
		if len(embeds) > 0:
			for embed in embeds:
				await ctx.send(embed=embed)
			

	def getRandSauce(self, amount, numbers):
		num = amount
		embeds = []
		if num > 0:
			# make sure num is not greater than how many numbers there are
			if num > len(numbers):
				num = len(numbers)
			# get random sauces: limit is len(numbers) and num amount
			i = 0
			while len(numbers) > 0 and i < num:
				# get a random sauce from numbers
				rand = choice(numbers)
				print(rand, end = " ")
				sauce = Sauce(rand)
				"""
				# do NOT submit loli or shota sauce
				while sauce.isIllegal():
					numbers.remove(rand)
					rand = choice(numbers)
					sauce = Sauce(rand)
				"""
				embeds.append(sauce.getEmbed())
				# make sure there are no duplicates
				numbers.remove(rand)
				i += 1
			print()
		return embeds