import discord
from random import randint

from pasta.helpers.nsfw.hentai.sauce import Sauce
from pasta.helpers.nsfw.search import Search

class randomSearch:
	def __init__(self):
		pass
	
	async def noArgs(self, ctx):
		await ctx.send("Fetching random sauce...")
		sauce = Sauce(str(randint(10000, 999999)))
		# make sure it exists
		while (not sauce.doesExist()) or sauce.isIllegal():
			sauce = Sauce(str(randint(10000, 999999)))

		await ctx.send(embed=sauce.getEmbed())
	
	async def yesArgs(self, ctx, data):
		category = data[0].lower()
		info = data[1].lower()
		await ctx.send("Random search for *{category}* - *{info}*...".format(category=category, info=info))
		search = Search(category, info)
		embed = search.getRandSauce()
		# make sure the embed will be valid
		if search.doesExist() and not embed is None:
			await ctx.send(embed=embed)
		else:
			await ctx.send("Found no *{category}* for *{info}*".format(category=category, info=info))