def getToken():
	file = open("../TOKEN.txt")
	token = file.read()
	file.close()
	return token