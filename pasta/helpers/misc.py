"""
Miscellaneus functions used by commands.py and events.py
"""

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def isCommand(content):
	commands = [".ignore", ".owo", ".uwu", ".shutdown", ".clean", ".readme", ".help", ".triggers", ".i", ".surprise"]
	for command in commands:
		if content.startswith(command):
			return True
	return False
	
def getTriggers():
	lines = []
	file = open("{this}/triggers.txt".format(this=THIS_FOLDER), "r")
	for line in file:
		# remove '\n'
		line = line[:-1]
		lines.append(line)
	
	file.close()
	return lines