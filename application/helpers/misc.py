# @author Sadeli
"""
Miscellaneus functions used by many commands and events
"""

import os
import datetime
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# list of all commands
def isCommand(content):
	commands = [".help", ".h", ".ignore", ".i", ".triggers", ".trigger", ".search", ".random", ".owo", ".uwu", ".clean", ".broadcast", ".log", ".shutdown"]
	for command in commands:
		if content.startswith(command):
			return True
	return False

# get list of trigger words for copypasta	
def getTriggers():
	try:
		lines = []
		file = open("{this}/triggers.txt".format(this=THIS_FOLDER), "r")
		for line in file:
			# remove '\n'
			line = line[:-1]
			lines.append(line)
		
		file.close()
		return lines
	except:
		print("triggers.txt not found")
		exit(1)

def timestamp():
	now = datetime.datetime.now()
	print("timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S"))
	print()