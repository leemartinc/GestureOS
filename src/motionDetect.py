from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import imutils
import time
from math import sqrt
import cv2

camera = PiCamera()
camera.resolution = (1280,960)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(1280,960))

print("[INFO] warming up...")

time.sleep(1)
avg = None
motionCounter = 0
frameNumber = 1
objectCount = 0
diffList = []
lastDecision = "nothing"
decisionList = []
startPayingAttention = False
decision = "nothing"
fartherCount = 0
closerCount = 0
finalDecision = ""

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
	frame = f.array
 
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	if avg is None:
                
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		
		print("[INFO] All ready!")

		continue
 
	cv2.accumulateWeighted(gray, avg, 0.6) # Adjust this value (update speed, contributes to sensitivity)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1] # Color limit
	thresh = cv2.dilate(thresh, None, iterations=2)

	whitePoints = cv2.findNonZero(thresh)

	# DECISION MAKING PART

	if not isinstance(whitePoints, type(None)):

		whitePoints = cv2.findNonZero(thresh).tolist()
		xValues = []

		for doubleList in whitePoints:

			for list in doubleList:

				xValues.append(list[0])
		
		minimum = min(xValues)
		maximum = max(xValues)

		difference = maximum - minimum

		diffList.append(difference)

		print("Last decision: " + lastDecision)

		if not len(diffList) == 1:
			if diffList[1] < diffList[0]:
				decision = "closer"
			elif diffList[1] > diffList[0]:
				decision = "farther"
			else:
				decision = "same"
			del diffList[0]

	else:

		decision = "nothing"
	
	# DECISION TRACKING PART

	print("Current decision: " + decision)
		
	if lastDecision == "nothing" and decision != "nothing":
	
		startPayingAttention = True

		print("Nothing, something met")

	if lastDecision != "nothing" and decision == "nothing":

		startPayingAttention = False
		print("List finished, here is it: " +  str(decisionList))

		for word in decisionList:
			if word == "farther":
				fartherCount += 1
			elif word == "closer":
				closerCount += 1

		if fartherCount > closerCount:
			finalDecision = "farther"
		elif fartherCount < closerCount:
			finalDecision = "closer"

		decisionList = []
		
	if startPayingAttention == True:

		decisionList.append(decision)
		print("added decision to list")

	lastDecision = decision

	print("Frame " + str(frameNumber))
	frameNumber = frameNumber + 1
	#print("Number of objects " + str(objectCount))
	objectCount = 0
	#print(centerList)

	rawCapture.truncate(0)
