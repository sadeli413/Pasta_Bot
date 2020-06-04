"""
A single sauce has numbers, a webpage response, and the doujin info
"""

import discord
import requests
# from pasta.helpers.nhentai import Nhentai
from pasta.helpers.nsfw.hentai.doujin import Doujin
from re import split

class Sauce:
	def __init__(self, number):
		self.number = number
		self.response = requests.get("https://nhentai.net/g/" + self.number)
		self.dj = (Doujin(number, self.response.text))
	
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
		# artists
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