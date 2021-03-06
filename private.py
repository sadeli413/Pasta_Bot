# @author Sadeli

# get bot token
def getToken():
	try:
		file = open("../TOKEN.txt")
		token = file.read()
		file.close()
		return token
	except:
		print("TOKEN.txt not found")
		exit(1)

# get bot owner's discord ID
def getID():
	try:
		file = open("../ID.txt")
		id = file.read()
		file.close()
		return int(id)
	except:	
		print("ID.txt not found")
		exit(1)

# get broadcast channel's ID
def getBroadcastID():
	try:
		file = open("../BROADCAST.txt")
		broadcast = file.read()
		file.close()
		return int(broadcast)
	except:
		print("BROADCAST.txt not found")
		return None