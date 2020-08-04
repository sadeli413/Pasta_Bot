# @author Sadeli
"""
A single sauce has numbers, a webpage response, and the doujin info
"""

import discord
import requests

class Sauce:
	def __init__(self, number):
		self.number = number
		self.response = requests.get("https://nhentai.net/api/gallery/" + self.number)
		self.data = self.response.json()
		self.isIllegal = False
		if self.doesExist():
			self.doujin = self.getDoujin()
	
	def doesExist(self):
		return self.response.status_code == 200
	
	# an embed of Title, url, Artists, Sauce, Pages, Tags, and Parodies	
	def getEmbed(self):
		self.checkIllegal(self.list2str(self.doujin["tags"])) # check if tags have loli or shota
		# embed the title and url
		title = self.doujin["title"] if len(self.doujin["title"]) <= 256 else self.doujin["title"][:253] + "..." # title has max length 256
		embed = discord.Embed(
			title = "`{name}`".format(name=title),
			url = None if self.isIllegal else "https://nhentai.net/g/" + self.number,
			colour = discord.Colour.red() if self.isIllegal else discord.Colour.blue() # doujins are blue. illegal doujins are red
		)
		embed.add_field(name = "SAUCE: ", value = self.number, inline=False)
		
		# only attatch num pages if they exist
		if self.doujin["pages"] > 0:
			embed.add_field(name = "PAGES: ", value = self.doujin["pages"], inline=False)
		
		# only attatch tags if they exist
		if len(self.doujin["tags"]) > 0:
			tags = self.ensureLen(self.doujin["tags"], 1018) # 1024 - 6 = 1018
			embed.add_field(name = "TAGS: ", value = tags, inline=False)
		
		# only attatch artists if they exist
		if len(self.doujin["artists"]) > 0:
			artists = self.ensureLen(self.doujin["artists"], 247) # 256 - 9
			embed.set_author(name = "ARTISTS: " + artists)

		# only attach parodies if they exist
		if len(self.doujin["parodies"]) > 0:
			parodies = self.ensureLen(self.doujin["parodies"], 1014) # 1024 - 10
			embed.add_field(name = "PARODIES: ", value = parodies, inline=False)

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
		# filter json to get data I actually want
		for key in self.data["tags"]:
			if key["type"] in validtypes:
				# add name and count to appropriate dictionary key
				out = "{name} ({count})".format(name=key["name"], count=key["count"])
				doujin[key["type"] + "s"].append(out)
		
		# rename parodys to parodies
		doujin["parodies"] = doujin.pop("parodys")

		return doujin 

	# ensure a maximum length
	def ensureLen(self, array, max):
		arr = array # can't change params, so make a copy
		string = self.list2str(arr)
		if (len(string) >= max - 5):
			while (len(string) >= max - 5): # -5 for ", etc"
				arr.pop()
				string = self.list2str(arr)
			string += ", etc"
		return string

	def list2str(self, array):
		return ", ".join(array)
		
		"""
# ensure maximum length 256
			artists = self.list2str(self.doujin["artists"])
			# max length 242 to include len 14 "ARTISTS: " and ", etc"
			while (len(artists) >= 242): # total number of characters
				self.doujin["artists"].pop()
				artists = self.list2str(self.doujin["artists"])
			artists += ", etc"
		"""