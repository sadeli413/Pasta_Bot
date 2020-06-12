"""
Randomly searches for a doujin. does NOT grab doujins with "loli" or "shota" in the tags
"""
import discord
from random import randint
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
		while (not sauce.doesExist()) or sauce.isIllegal():
			sauce = Sauce(str(randint(10000, 999999)))

		await ctx.send(embed=sauce.getEmbed())
	
	# get amount sauce of a search criteria
	async def yesArgs(self, ctx, amount, criteria):
		find = Search(criteria)
		embeds = find.getRandSauce(amount)
		# make sure the embed will be valid
		if find.doesExist() and len(embeds) > 0:
			for embed in embeds:
				await ctx.send(embed=embed)
		elif find.doesExist() and len(embeds) < amount:
			await ctx.send("||Unfortunately, {rm} doujin(s) have been removed from your request because too many lolis/shotas (see .readme for more)||".format(rm=amount-len(embeds)))
		else:
			await ctx.send("Found no `{criteria}` ||Or it's all loli/shota||".format(criteria=criteria))
