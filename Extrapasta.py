class Extrapasta:
	# for owo
	last = ""
	# navy seals copypasta
	sealFile = open("pastas/fuck.txt", "r")
	SEAL_TEXT_LOWER = sealFile.read().lower()
	sealFile.close()

	# navy seals response pasta
	responseFile = open("pastas/extra/navySealResponse.txt", "r")
	SEAL_RESPONSE = responseFile.read()
	responseFile.close()

	# too much hentai copypasta
	tooMuchFile = open("pastas/extra/tooMuchHentai.txt", "r")
	TOOMUCH_TEXT = tooMuchFile.read()
	tooMuchFile.close()

	# FBI OPEN UP when searching for loli or shota content
	fbiFile = open("pastas/extra/fbiOpenUp.txt", "r")
	FBI_TEXT = fbiFile.read()
	fbiFile.close()
	
	# display the tooMuchHentai message
	def tooMuchHentai():
		return Extrapasta.TOOMUCH_TEXT
	
	# notify if there's loli or shota content
	def fbiOpenUp():
		return Extrapasta.FBI_TEXT
	
	# navy seal response
	def sealResponse(content):
		# check if the content equals the navy seal response
		if Extrapasta.SEAL_TEXT_LOWER in content:
			return Extrapasta.SEAL_RESPONSE
			
		return ""
		
	def owoify(words):
		return words.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
		
		