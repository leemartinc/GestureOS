"""
   Copyright 2017 Charlie Liu and Bryan Zhou

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (256, 256)
rawCapture1 = PiRGBArray(camera, size = camera.resolution)
rawCapture2 = PiRGBArray(camera, size = camera.resolution)

time.sleep(1)

diffList = []

zoomFactorList = []

currentStatusChange = None
lastStatusChange = None
statusList = []

inMotion = False

fartherCount = 0
closerCount = 0

finalDecision = None

camera.capture(rawCapture1, format = "bgr", use_video_port = True)

frame1 = rawCapture1.array

gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)

rawCapture1.truncate(0)

while True:

	camera.capture(rawCapture2, format = "bgr", use_video_port = True)
	
	frame2 = rawCapture2.array

	gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

	blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)

	diffImg = cv2.absdiff(blur1, blur2)

	thresh = cv2.threshold(diffImg, 20, 255, cv2.THRESH_BINARY)[1]

	whitePoints = cv2.findNonZero(thresh)

	if whitePoints is not None:

		whitePoints = cv2.findNonZero(thresh).tolist()

		xValues = []

		for doubleList in whitePoints:

			for list in doubleList:

				xValues.append(list[0])

		for item in xValues:

                        xValueDifference = xValues[item-1] - xValues[item-2]

                        xValueDiffList.append(xValueDifference)

                del xValueDiffList[0]
		
		minimum = min(xValues)
		maximum = max(xValues)

		difference = maximum - minimum

		diffList.append(difference)

		if len(diffList) != 1:

			if diffList[1] < diffList[0]:

				currentStatusChange = "closer"

                                for item in xValueDiffList:

                                        zoomFactor = xValueDiffList(item-1) / diffList[1]

                                        zoomFactorList.append(zoomFactor)

			elif diffList[1] > diffList[0]:

				currentStatusChange = "farther"

				for item in xValueDiffList:

                                        zoomFactor = "/" + str(xValueDIffList(item-1) / diffList[1])

                                        zoomFactorList.append(zoomFactor)

			else:

				currentStatusChange = "same"

			del diffList[0]
			xValues = []
                        xValueDiffList = []

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

		if finalDecision == "farther":

                        for item in zoomFactorList:

                                fileName = "info/" + str(int(time.time())) + "_f" + str(zoomFactorList[item-1])

			open(fileName, "a").close()
		
		elif finalDecision == "closer":

                        for item in zoomFactorList:

                                fileName = "info/" + str(int(time.time())) + "_c" + str(zoomFactorList[item-1])

			open(fileName, "a").close()

		fartherCount = 0
		closerCount = 0

		statusList = []

		print("Hand gesture detected! Motion is: " + finalDecision)

        zoomFactorList = []

	lastStatusChange = currentStatusChange

	blur1 = blur2

	rawCapture2.truncate(0)
