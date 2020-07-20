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
		self.doujin = self.getDoujin()
	
	def doesExist(self):
		return self.response.status_code == 200
	
	# an embed of Title, url, Artists, Sauce, Pages, Tags, and Parodies	
	def getEmbed(self):
		self.checkIllegal(self.list2str(self.doujin["tags"]))
		embed = discord.Embed(
			title = "`{name}`".format(name=self.doujin["title"]),
			url = None if self.isIllegal else "https://nhentai.net/g/" + self.number,
			colour = discord.Colour.red() if self.isIllegal else discord.Colour.blue()
		)
		
		# sauce-numbers, pages, and tags
		embed.add_field(name = "SAUCE: ", value = self.number, inline=False)
		embed.add_field(name = "PAGES: ", value = self.doujin["pages"], inline=False)
		
		#only attatch tags if they exist
		if len(self.doujin["tags"]) > 0:
			embed.add_field(name = "TAGS: ", value = self.list2str(self.doujin["tags"]), inline=False)
		
		# only atatch artists if they exist
		if len(self.doujin["artists"]) > 0:
			embed.set_author(name = "ARTISTS: " + self.list2str(self.doujin["artists"]))

		# only attach parodies if they exist
		if len(self.doujin["parodies"]) > 0:
			embed.add_field(name = "PARODIES: ", value = self.list2str(self.doujin["parodies"]), inline=False)

		return embed
		
	def checkIllegal(self, tags):
		self.isIllegal = "loli" in tags or "shota" in tags

	def getDoujin(self):
		doujin = {
			"title": self.data["title"]["pretty"],
			"tags": [],
			"artists": [],
			"parodys": [], # purposeful mispelling
			"pages": self.data["num_pages"]
		}
		# types into dictionary	
		validtypes = ["tag", "artist", "parody"]
		for key in self.data["tags"]:
			if key["type"] in validtypes:
				out = "{name} ({count})".format(name=key["name"], count=key["count"])
				doujin[key["type"] + "s"].append(out)
		
		# rename parodys to parodies
		doujin["parodies"] = doujin.pop("parodys")

		return doujin 
	
	def list2str(self, arr):
		return ", ".join(arr)