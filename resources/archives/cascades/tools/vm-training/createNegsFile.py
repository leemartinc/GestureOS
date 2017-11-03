import os

def createNegativeFile():

	dir = "negs"

	for img in os.listdir(dir):

		text = dir + "/" + img + "\n"

		with open("bg.txt", "a") as file:

			file.write(text)

createNegativeFile()
