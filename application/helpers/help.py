# @author Sadeli
"""
A help message has usage, description, and examples
"""
import discord

class Help:
	def __init__(self):
		self.help = message(
			".help [command]",
			"DM a help message",
			"")
		self.ignore = message(
			".ignore",
			"Pasta_Bot will ignore messages beginning with .ignore or .i",
			"")
		self.owo = message(
			".owo [@user_mention] [@user_mention] [...]", 
			"Owoify the last message in channel or by mentioned users with .owo or .uwu",
			"")
		self.clean = message(
			".clean",
			"Only available for those with Manage Messages permissions\nOf the past two hundred messages delete messages sent by Pasta_Bot",
			"")
		self.triggers = message(
			".triggers",
			"DM a message containing all copypasta trigger words",
			"")
		self.random = message(
			".random [amount] [search criteria]",
			"Send a random hentai with optional criteria",
			"\n__.random 3__\n*(gets 3 random hentai)*\n\n__.random 2 character:\"momo velia deviluke\" stockings -rape__\n*(gets 2 random doujins with character momo and tags stockings without rape)*")
		self.search = message(
			".search [amount] {search criteria}",
			"Send the top results for a hentai search criteria",
			"\n__.search artist:hiten nakadashi paizuri -rape__ \n*(gets the top result for artist hiten and tags paizuri and nakadashi without rape)*\n\n__.search 2 artist:shindol__\n*(gets top 2 results for artist shindol)*")
		self.botDictionary = {
			".help": self.help,
			".ignore": self.ignore,
			".owo": self.owo,
			".clean": self.clean,
			".triggers": self.triggers,
			".random": self.random,
			".search":self.search
		}
		# all help message
		self.msg = self.sendMessage()
	
	def sendMessage(self):
		msg = "Pasta_Bot is free and open source. View documentation and source code at:\n https://github.com/sadeli413/Pasta_Bot.git\n\n"
		msg += "Add Pasta_Bot to your server:\n https://discord.com/api/oauth2/authorize?client_id=715018649588727859&permissions=8&scope=bot\n\n"
		msg += "```css\nPasta_Bot\nCommands [optional] {required}\n\n"
		for cmd in self.botDictionary.values():
			msg += cmd.usage+"\n"
			msg += cmd.description+"\n\n"
		msg += "Other features include triggering copypastas from keywords and triggering hentai from five or six digit numbers"
		msg += "```"
		return msg

class message:
	def __init__(self, usage, description, example):
		self.usage = usage
		self.description = description
		self.example = example
		# individual help message
		self.embed = discord.Embed(title = self.usage, colour = discord.Colour.green())
		self.embed.add_field(name = "DESCRIPTION", value = self.description, inline=False)
		if len(self.example) > 0:
			self.embed.add_field(name = "EXAMPLES", value = self.example, inline=False)
