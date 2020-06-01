"""
A doujin has a Title, url, html text, Artists, numbers, Pages, Tags, and Parodies
"""


from re import split

class Doujin:
	def __init__(self, number, html):
		 self.number = number
		 self.html = html
		 self.url = "https://nhentai.net/g/" + self.number

	# return the title as a string. note that the title is found in the metadata
	def getTitle(self):
		# find the line with the title
		head = "<meta name=\"twitter:title\" content="
		line = self.getLine(head)
		line = line[len(head) + 2 : -4]
		# make sure the title is a printable character
		title = ""
		for char in line:
			if " " <= char and char <= "~":
				title += char
		# weird ascii code for apostrophe 
		apostrophe = "&#39;"
		title = title.replace("&#39;", "\'")
		
		return title

	# return the tags as a string. note that the tags are found in the metadata
	def getTags(self):
		# find the line with the tags
		head = "<meta name=\"twitter:description\" content="
		line = self.getLine(head)
		line = line[len(head) + 2 : -4]
		
		tags = line.split(", ")
		return self.list2str(tags)
		
	# return the authors as a string. note that the authors are NOT found in the metadata	
	def getArtists(self):
		head = "<span class=\"tags\"><a href=\"/artist/"
		line = self.getLine(head)
		# delete everything before >
		return self.getSpan(line)

	# return the authors as a string. note that the parodies are NOT found in the metadata
	def getParodies(self):
		head = "<span class=\"tags\"><a href=\"/parody/"
		line = self.getLine(head)
		if len(line) > 0:
			return self.getSpan(line)
		
		# Return nothing if there are no parodies
		return ""

	def getPages(self):
		tail = "pages</div>"
		line = self.getLine(tail)
		return line[9:-12]

	# return the data of a line as a string
	def getSpan(self, line):
		# split the line up from the html tags < and >
		words = split("[<>]", line)
		data = []
		# the necessary data is only found starting on the 4th index every 8 items
		for i in range(4, len(words), 8):
			data.append(words[i][:-1]) # append and remove a space

		# last item of parodies is always just an empty string
		data.pop()
		return self.list2str(data)
	
	# looks for a head in a line of html
	def getLine(self, head):
		for line in self.html.split('\n'):
			if head in line:
				return line
		return ""
		
	# "converts, a, list, into, a, string, like, this"
	def list2str(self, list):
		out = ""
		for word in list:
			out += word + ", "
		
		return out[:-2]