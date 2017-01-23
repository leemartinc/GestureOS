from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (1280,960)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size = (1280,960))

time.sleep(1)

avg = None

diffList = []

currentStatusChange = None
lastStatusChange = None
statusList = []

inMotion = False

fartherCount = 0
closerCount = 0

finalDecision = None

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
        
	frame = frame.array

	frame = cv2.resize(frame, (500, 500))

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	if avg is None:
                
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		
		print("[INFO] Setup complete!")

		continue
 
	cv2.accumulateWeighted(gray, avg, 0.6) # Adjustable value for accuracy
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1] # Adjustable value for accuracy
	thresh = cv2.dilate(thresh, None, iterations = 2)

	whitePoints = cv2.findNonZero(thresh)

	if whitePoints is not None:

		whitePoints = cv2.findNonZero(thresh).tolist()

		xValues = []

		for doubleList in whitePoints:

			for list in doubleList:

				xValues.append(list[0])
		
		minimum = min(xValues)
		maximum = max(xValues)

		difference = maximum - minimum

		diffList.append(difference)

		if len(diffList) != 1:

			if diffList[1] < diffList[0]:

				currentStatusChange = "closer"

			elif diffList[1] > diffList[0]:

				currentStatusChange = "farther"

			else:

				currentStatusChange = "same"

			del diffList[0]
	
	else:

		currentStatusChange = None
	
	if inMotion is True:

		statusList.append(currentStatusChange)
		
	if lastStatusChange is None and currentStatusChange is not None:
	
		inMotion = True

	elif lastStatusChange is not None and currentStatusChange is None:

		inMotion = False

		for status in statusList:

			if status == "farther":

				fartherCount += 1

			elif status == "closer":

				closerCount += 1

		if fartherCount > closerCount:

			finalDecision = "farther"

		elif closerCount > fartherCount:

			finalDecision = "closer"
		
		else:

			finalDecision = "unsure"

		fartherCount = 0
		closerCount = 0

		statusList = []

		print("Hand gesture detected! Motion is: " + finalDecision)

		pipe = open("statusChange", "w")

		pipe.write(finalDecision)

		pipe.close()

	lastStatusChange = currentStatusChange

	rawCapture.truncate(0)
