# Pasta_Bot
Pasta_Bot v1.0.1\
A NSFW Discord bot made by Sadeli.
- Join the [Pasta_Bot server!](https://discord.gg/KhRBjpT)
- [Invite Pasta_Bot](https://discord.com/api/oauth2/authorize?client_id=715018649588727859&permissions=2147483383&scope=bot) to your own server!
- Pasta_Bot is free and open source. [Click here](https://github.com/sadeli413/Pasta_Bot.git) to learn about recursion, view source code, and read documentation.

---
## Table of Contents
- [Commands](#commands)
	- [.help](#help)
	- [.ignore](#ignore)
	- [.owo](#owo)
	- [.clean](#clean)
	- [.triggers](#triggers)
	- [.random](#random)
	- [.search](#search)
- [On Message Event](#on-message-event) 
	- [hentai](#hentai)
	- [copypasta](#copypasta)
- [Owner Commands](#owner-commands)
- [Other](#other)
- [Citations](#citations)
- [Porting Pasta_Bot](#how-to-port-pasta_bot)
- [Notes](#notes-from-sadeli)

---

## Commands
[] means optional arguments\
{} means required argument

### HELP
- DESCRIPTION: DM a help message
- USAGE: ```.help [command]```
- Alias: ```.h```

### IGNORE
- DESCRIPTION: Pasta_Bot will NOT read or act on any messages beginning with .ignore
- USAGE: ```.ignore [any message here]```
- Alias: ```.i```

### OWO 
- DESCRIPTION: Without arguments, owoify the last message in the channel. Mention one or more users as arguments to owoify their last message.
- USAGE: ```.owo [@user_mention] [@user_mention] [...]```
- Alias: ```.uwu```

### CLEAN
- DESCRIPTION: Of the past 200 messages in channel history, delete messages sent by Pasta_Bot
- USAGE: ```.clean```
- NOTES: Can only be used by users with Manage Messages permissions

### TRIGGERS
- DESCRIPTION: DM a message containing all copypasta trigger words
- USAGE: ```.triggers```
- Alias: ```.trigger```

### RANDOM
- DESCRIPTION: Send a random hentai. If an amount is specified, send that amount (no maximum). If a search criteria is specified, then search under that criteria (maximum amount 25)
- USAGE: ```.random [amount] [search criteria]```
- NOTES: This searches the 25 most popular search results. For search criteria help, visit https://nhentai.net/info/ *This is the slowest command, since it randomly searches until it finds a doujin that exists*.
	
### SEARCH
- DESCRIPTION: Send the top result of a nhentai link with a given search. Optional: specify an amount of links. 
- USAGE: ```.search [amount] {search criteria}```
- NOTES: 25 maximum amount searched. Any higher amount will automatically default to 25.
For search criteria help, visit https://nhentai.net/info/
*This command tends to be slow since it involves web get requests.*

---

## On message event
If triggered, give hentai.
If no hentai is triggered, then give a copypasta based on a copypasta trigger

### HENTAI
- DESCRIPTION: Triggered by five or six digit numbers in a message. Provides the following:
	- Artist(s) (if applicable)
	- Title
	- Link to nhentai page (omit link and make the embed red if the tags include "loli" or "shota")
	- Sauce provided in message (the triggering five or six digit numbers)
	- Number of Pages
	- Tag(s)
	- Parodies (if applicable)

OTHER FEATURES: Pasta_Bot will send a kink shame copypasta if you submit 4 or more sauces in one message. Additionally, Pasta_Bot will kink shame you if one of the tags include *loli* or *shota*.
No embed will be sent if the numbers returns a 404 status code. Unlike .search or .random, this feature sends the message AFTER all hentai is found, whereas .search and .random search and send hentai one at a time. *This feature tends to be slow since it runs a web request.*
	
### COPYPASTA
- DESCRIPTION: Triggered by the last keyword of a message. Use TRIGGERS command for a list of triggers
- OTHER FEATURES: I will respond to the Navy Seals copypasta with the response copypasta

---

## Owner Commands
These Pasta_Bot commands are only allowed to be executed by the bot owner.

### BROADCAST
- DESCRIPTION: Send a message to your broadcast channel. Your channel ID should go into BROADCAST.txt
- USAGE: ```.broadcast [any message here]```

### LOG
- DESCRIPTION: DMs the owner a list of all guilds Pasta_Bot is a member of.
- USAGE: ```.log```

### SHUTDOWN
- DESCRIPTION: Logs out the bot and terminates the program.
- USAGE: ```.shutdown```

---

## Other

### STATUS
- DESCRIPTION: Every 5 minutes as a background task, Pasta_Bot will change statuses.

---

## Citations

### ICON
I do not own the Araragi Tsukihi icon. Source is Monogatari Series.

### COPYPASTAS
I did not create most of these copypastas. Most of these copypastas were taken from https://www.reddit.com/r/copypasta/

### HENTAI
All hentai is taken from https://nhentai.net and their glorious api.

### DISCORD
Made with [discord.py](https://discordpy.readthedocs.io/en/latest/)

---

## How to port Pasta_Bot
**PYTHON 3 IS REQUIRED**
1. [Create a bot account](https://discordpy.readthedocs.io/en/latest/discord.html) and get your bot token.
2. Download [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html)
3. clone this repository with:
```
git clone https://github.com/sadeli413/Pasta_Bot.git
```
4. Outside of the Pasta_Bot/ folder, create 3 text files **ID.txt**, **TOKEN.txt**, and **BROADCAST.txt**. **BROADCAST.txt** is optional.
5. Put your discord ID inside of **ID.txt**, your bot token inside of **TOKEN.txt**, and your discord broadcast channel's ID inside of **BROADCAST.txt**.

Your tree should look something like this:
```
|BROADCAST.txt
|ID.txt
|TOKEN.txt
|Pasta_Bot/
|___application/
|___pasta_bot.py
|___private.py
|___README.md
```

6. Go into Pasta_Bot/ folder and run Pasta_Bot with:
```
python3 pasta_bot.py
```
On Windows it would be:
```
python pasta_bot.py
```

---

## Notes from Sadeli:

- I do not want this on my main github, so sadeli413 is my alternate github account. Come check out my main github at: https://github.com/thad-shinno

- Although this is kind of a useless bot, please give it lots of headpats and [invite it to lots of servers](https://discord.com/api/oauth2/authorize?client_id=715018649588727859&permissions=2147483383&scope=bot). It's a very lewd bot. If it's too annoying, have your admin remove it's priveleges in select channels.

- Pasta_Bot is FOSS. Feel free to port it, or copy and use the code. It would be cool if you credited me.

- Pasta_Bot is not licensed, but that's subject to change.

- This is a hobby project to improve my coding skills. If you see terrible code or bugs in Pasta_Bot, please let me know on the [Pasta_Bot server](https://discord.gg/KhRBjpT).

- I know, I know. I should implement cogs. When I find more time, I'll do that. It *does* seem like it would make the bot more organized.

Thank you for using Pasta_Bot.

\- by Sadeli