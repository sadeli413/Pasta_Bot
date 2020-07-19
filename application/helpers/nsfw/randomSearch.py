"""
Randomly searches for a doujin. does NOT grab doujins with "loli" or "shota" in the tags
"""
import discord
from random import randint
from random import choice
# custom packages
from application.helpers.nsfw.hentai.sauce import Sauce
from application.helpers.nsfw.search import Search

class randomSearch:
	def __init__(self):
		pass
	
	# get one random sauce
	async def noArgs(self, ctx):
		print("fetching...")
		sauce = Sauce(str(randint(10000, 999999)))
		# make sure it exists
		while (not sauce.doesExist()):
			sauce = Sauce(str(randint(10000, 999999)))

		await ctx.send(embed=sauce.getEmbed())
	
	# get amount sauce of a search criteria
	async def yesArgs(self, ctx, amount, criteria):
		find = Search(criteria)
		embeds = self.getRandSauce(amount, find.getNumbers())
		# make sure the embed will be valid
		if find.doesExist() and len(embeds) > 0:
			for embed in embeds:
				await ctx.send(embed=embed)
		else:
			await ctx.send("Found no `{criteria}`".format(criteria=criteria))

	def getRandSauce(self, amount, numbers):
		num = amount
		embeds = []
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
		return embeds