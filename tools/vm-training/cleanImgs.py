import numpy as np
import cv2
import os

def findInvalids():
    
	searchDir = "negs"
	invalidDir = "invalids"

	for img in os.listdir(searchDir):

		for invalid in os.listdir(invalidDir):

			try:

				imgPath = searchDir + "/" + str(img)
				invalidImg = cv2.imread(invalidDir + "/" + str(invalid))
				testingImg = cv2.imread(imgPath)

				if invalidImg.shape == testingImg.shape and not(np.bitwise_xor(invalidImg, testingImg).any()):

					os.remove(imgPath)
					
					print("Invalid image " + imgPath + " has been deleted")

			except Exception as e:

				print(str(e))

findInvalids()
