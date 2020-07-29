# @author Sadeli

# get bot token
def getToken():
	file = open("../TOKEN.txt")
	token = file.read()
	file.close()
	return token

# get bot owner's discord ID
def getID():
	file = open("../ID.txt")
	id = file.read()
	file.close()
	return int(id)
