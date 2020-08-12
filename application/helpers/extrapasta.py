# @author Sadeli
"""
Description: Extra copypastas not triggered by trigger words
"""

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# navy seals copypasta
try:
	sealFile = open(THIS_FOLDER + "/pastas/fuck.txt", "r")
	SEAL_TEXT_LOWER = sealFile.read().lower()
	sealFile.close()
except:
	print("could not open/close fuck.txt")
	exit(1)

# navy seals response pasta
try:
	responseFile = open(THIS_FOLDER + "/pastas/extra/navySealResponse.txt", "r")
	SEAL_RESPONSE = responseFile.read()
	responseFile.close()
except:
	print("could not open/close navySealResponse.txt")
	exit(1)

# too much hentai copypasta
try:
	tooMuchFile = open(THIS_FOLDER + "/pastas/extra/tooMuchHentai.txt", "r")
	TOOMUCH_TEXT = tooMuchFile.read()
	tooMuchFile.close()
except:
	print("could not open/close tooMuchHentai.txt")
	exit(1)

# FBI OPEN UP when searching for loli or shota content
try:
	fbiFile = open(THIS_FOLDER + "/pastas/extra/fbiOpenUp.txt", "r")
	FBI_TEXT = fbiFile.read()
	fbiFile.close()
except:
	print("could not open/close fbiOpenUp.txt")
	exit(1)

# display the tooMuchHentai message
def tooMuchHentai():
	return TOOMUCH_TEXT

# notify if there's loli or shota content
def fbiOpenUp():
	return FBI_TEXT

# navy seal response
def sealResponse(content):
	# check if the content equals the navy seal response
	if SEAL_TEXT_LOWER in content:
		return SEAL_RESPONSE
		
	return ""
