"""
# Title: Copypasta.py
# Author: Thad Shinno
# Description: class that sends a copypasta based on the last keyword in a lowercase discord message. There are some copypasta exceptions
"""
from re import split

class Copypasta:
	# return a string copypasta based on a full message content
	def getPasta(content):
		# an array of triggers. check for new content each time.
		TRIGGERS = Copypasta.getTriggers()
		# copypasta the last trigger word in the content
		reversedContent = reversed(split("[^a-z^A-Z^0-9]", content))
		for word in reversedContent:
			for trigger in TRIGGERS:
				if trigger in word:
					return Copypasta.file2pasta(trigger)
				
		# if there's no copypasta, then return an empty string
		return ""
	
	def getTriggers():
		return Copypasta.file2list("triggers.txt")
	
	# return a list of triggers
	def file2list(filename):
		lines = []
		file = open(filename, "r")
		
		for line in file:
			# remove '\n'
			line = line[:-1]
			lines.append(line)
		
		file.close()
		return lines

	# return the text content of pastas/trigger.txt
	def file2pasta(trigger):
		filename = "pastas/" + trigger + ".txt"
		file = open(filename, "r")
		text = file.read()
		file.close()
		return text