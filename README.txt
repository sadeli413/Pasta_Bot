README
Pasta_Bot
	DESCRIPTION: A NSFW Discord bot made by Thad Shinno.
	https://github.com/sadeli413/Pasta_Bot.git

*****************************************************************************************************************************************
Commands:
[] means optional arguments
<> means required argument

HELP (NOT YET IMPLEMENTED)
	DESCRIPTION: DM a help message
	USAGE: .help

IGNORE
	DESCRIPTION: Pasta_Bot will NOT read or act on any messages beginning with .ignore
	USAGE: .ignore [any message here]
	Alias: .i

TRIGGERS
	DESCRIPTION: DM a message containing all copypasta trigger words
	USAGE: .triggers

OWO 
	DESCRIPTION: Without arguments, owoify the last message in the channel. Mention one or more users as arguments to owoify their last message.
	USAGE: .owo [@user_mention @user_mention...]
	Alias: .uwu

RANDOM
	DESCRIPTION: Send a random hentai of a keyword in a category. Without arguments, send a random nhentai link.
	USAGE: .random <category> <keyword>
	NOTE: This never sends hentai with tags including "loli" or "shota". *Additionally, this command tends to be slow since it involves a web request.*
	
CLEAN
	DESCRIPTION: Of the past 200 messages in channel history, delete messages sent by Pasta_Bot
	USAGE: .clean

README
	DESCRIPTION: DMs README.txt file for a full description of bot
	USAGE: .readme

*****************************************************************************************************************************************
On message:
If triggered, give hentai.
If no hentai is triggered, then give a copypasta based on a copypasta trigger

HENTAI
	DESCRIPTION: Triggered by five or six digit numbers in a message. Provides the following:
		- Artist(s)
		- Title
		- Link to nhentai page (omit link if the tags include "loli" or "shota")
		- Sauce provided in message (the triggering five or six digit numbers)
		- Number of Pages
		- Tag(s)
		- Parodies (if applicable)
	OTHER FEATURES: I will send a kink shame copypasta if you submit 4 or more sauces in one message.
					Additionally, I will kink shame you if one of the tags include *loli* or *shota*.
					No embed will be sent if the numbers returns a 404 status code.
					*Note that this feature tends to be slow since it runs a web request*
	
COPYPASTA
	DESCRIPTION: Triggered by the last keyword of a message. Use TRIGGERS command for a list of triggers
	OTHER FEATURES: I will respond to the Navy Seals copypasta with the response copypasta

*****************************************************************************************************************************************
Other:

STATUS:
	DESCRIPTION: Every 5 minutes as a background task, Pasta_Bot will change statuses in between
		"Watching lots of hentai"
		"Listening to sad loli asmr"

*****************************************************************************************************************************************
Citations:

ICON: I do not own the spaghetti-ahegao photo used for Pasta_Bot icon. The icon was taken from https://knowyourmeme.com/photos/1299418-ostagram-spaghetti-mashups
COPYPASTAS: I did not create most of these copypastas. Most of these copypastas were taken from https://www.reddit.com/r/copypasta/
HENTAI: All hentai is taken from https://nhentai.net/
DISCORD: Made with discord.py Documentation at https://discordpy.readthedocs.io/en/latest/
GITHUB: I do not want this on my main github so I added this to an alternate github account found at the top of this readme. My main github is at https://github.com/thad-shinno