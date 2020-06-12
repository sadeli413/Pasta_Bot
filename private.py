def getToken():
	file = open("../TOKEN.txt")
	token = file.read()
	file.close()
	return token

def getID():
	file = open("../ID.txt")
	id = file.read()
	file.close()
	return int(id)
