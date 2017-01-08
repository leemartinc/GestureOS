import urllib.request
import cv2
import sys
import os

def storeImages():
	
	imageLink = sys.argv[1]
	imageUrls = urllib.request.urlopen(imageLink).read().decode()

	directory = "negs"

	picNumber = len(os.listdir(directory)) + 1

	for url in imageUrls.split("\n"):

		try:

			imgName = directory + "/" + str(picNumber) + ".jpg"
			urllib.request.urlretrieve(url, imgName)

			img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
			resizedImg = cv2.resize(img, (150, 150))

			cv2.imwrite(imgName, resizedImg)
			picNumber += 1

			print("Saved image number " + str(picNumber) + " from " + url)

		except Exception as e:

			print(str(e))

storeImages()
