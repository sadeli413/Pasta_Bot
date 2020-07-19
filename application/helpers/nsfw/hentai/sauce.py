"""
A single sauce has numbers, a webpage response, and the doujin info
"""

import discord
import requests

class Sauce:
	def __init__(self, number):
		self.number = number
		# self.response = requests.get("https://nhentai.net/g/" + self.number)
		self.response = requests.get("https://nhentai.net/api/gallery/" + self.number)
		self.data = self.response.json()
		self.isIllegal = False
		# self.dj = Doujin(number, self.response.json())
	
	def doesExist(self):
		return self.response.status_code == 200
	
	# an embed of Title, url, Artists, Sauce, Pages, Tags, and Parodies	
	def getEmbed(self):
		
		doujin = self.getDoujin()
		bad = self.checkIllegal(self.list2str(doujin["tags"]))
		embed = discord.Embed(
			title = "`{name}`".format(name=doujin["title"]),
			url = None if bad else "https://nhentai.net/g/" + self.number,
			colour = discord.Colour.red() if bad else discord.Colour.blue()
		)
		
		# sauce-numbers, pages, and tags
		embed.add_field(name = "SAUCE: ", value = self.number, inline=False)
		embed.add_field(name = "PAGES: ", value = doujin["pages"], inline=False)
		
		#only attatch tags if they exist
		if len(doujin["tags"]) > 0:
			embed.add_field(name = "TAGS: ", value = self.list2str(doujin["tags"]), inline=False)
		
		# only atatch artists if they exist
		if len(doujin["artists"]) > 0:
			embed.set_author(name = "ARTISTS: " + self.list2str(doujin["artists"]))
		# only attach parodies if they exist
		if len(doujin["parodies"]) > 0:
			embed.add_field(name = "PARODIES: ", value = self.list2str(doujin["parodies"]), inline=False)

		return embed
		
	def checkIllegal(self, tags):
		self.isIllegal = "loli" in tags or "shota" in tags
		return self.isIllegal

	def getDoujin(self):
		doujin = {
			"title": self.data["title"]["pretty"],
			"tags": [],
			"artists": [],
			"parodys": [], # purposeful mispelling
			"pages": self.data["num_pages"]
		}
		validtypes = ["tag", "artist", "parody"]
		# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		for key in self.data["tags"]:
			#name = key["name"]
			if key["type"] in validtypes:
				doujin[key["type"] + "s"].append(key["name"])
		
		# rename parodys to parodies
		doujin["parodies"] = doujin.pop("parodys")

		return doujin 
	
	def list2str(self, arr):
		return str(arr)[1:-1]