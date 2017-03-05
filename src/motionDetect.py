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
import numpy
import cv2

# User defined experimental values

imgSize= 256
blurSize = 5
threshold = 10
sampleSize = 10
lowerOutlierCutOff = 25
upperOutlierCutOff = 150

# Camera parameters

camera = PiCamera()
camera.resolution = (imgSize,imgSize)
camera.color_effects = (128, 128)
rawCapture1 = PiRGBArray(camera, size = camera.resolution)
rawCapture2 = PiRGBArray(camera, size = camera.resolution)

time.sleep(0.1)

# Initializing detection variables

firstFrame = None
currentStatusChange = None

xAxis = []
actualDiffList = []
filteredDiffList = []
windowOfData = []
filteredWindowOfData = []

# Additional variables to define

#kernel_55 = numpy.ones((5,5), 'uint8')
frameCount = 1
fileName = ""

# Geting user input for some variables

maxFrames = int(input("Number of max frames?: "))

time.sleep(1)

# Taking the first capture

camera.capture(rawCapture1, format = "bgr", use_video_port = True)
frame1 = rawCapture1.array
gray1= cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
blur1 = cv2.GaussianBlur(gray1, (blurSize, blurSize), 0)

rawCapture1.truncate(0)

# Opening the data file

rawFile = open("data-raw.csv", "w")
filteredFile = open("data-filtered.csv", "w")

# Detection loop

while True:

	#print("Actual frame: " + str(frameCount))
	
	# Capturing a frame and modifying it

	camera.capture(rawCapture2, format = "bgr", use_video_port = True)
	
	frame2 = rawCapture2.array
	gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
	blur2 = cv2.GaussianBlur(gray2, (blurSize, blurSize), 0)
	
	diffImg = cv2.absdiff(blur1, blur2)

	thresh = cv2.threshold(diffImg, threshold, 255, cv2.THRESH_BINARY)[1]

	#thresh = cv2.dilate(thresh, kernel_55)
	#thresh = cv2.dilate(thresh, kernel_55)
	#thresh = cv2.erode(thresh, kernel_55)
	
	#im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#thresh = cv2.drawContours(thresh, contours, -1, (0,255,0), 3)

	# DEBUG: Showing the modified image

	#cv2.imshow("window", thresh)
	#cv2.waitKey(1)

	# Finding the farthest white points

	whitePoints = cv2.findNonZero(thresh)

	if whitePoints is not None:

		whitePoints = cv2.findNonZero(thresh).tolist()

		whitePointXValues = []

		for doubleList in whitePoints:

			for list in doubleList:

				whitePointXValues.append(list[0])

		minimum = min(whitePointXValues)
		maximum = max(whitePointXValues)
		difference = maximum - minimum

		actualDiffList.append(difference)

	else:

		actualDiffList.append(0)

	# Determining the gesture

	if len(actualDiffList) % sampleSize == 0:

		# Filtering outliers

		windowOfData = actualDiffList[len(actualDiffList) - sampleSize : len(actualDiffList)]
		filteredWindowOfData = []

		for item in windowOfData:

			if item > lowerOutlierCutOff and item < upperOutlierCutOff:

				filteredWindowOfData.append(item)
				filteredDiffList.append(item)
		
		if len(filteredWindowOfData) >= 2:
    			
			filteredWindowOfData.remove(max(filteredWindowOfData))
			filteredWindowOfData.remove(min(filteredWindowOfData))

		if len(filteredWindowOfData) <= 1:

			blur1 = blur2

			rawCapture2.truncate(0)

			# Frame counter checks and updates

			if frameCount >= maxFrames:

				break

			frameCount += 1
			
			continue

		#print("Length of filteredWindowOfData after filter: " + str(len(filteredWindowOfData)))
		
		#print("Length of filteredDiffList after adding: " + str(len(filteredDiffList)))
		
		for i in range(1, len(filteredWindowOfData) + 1):

			xAxis.append(i)
		
		if len(filteredWindowOfData) > 0:
		
			slope = numpy.polyfit(xAxis, filteredWindowOfData, 1)[0]

			# Making a decision

			if slope < -0.5:

				statusChange = "closer"
			
			elif slope > 0.5:

				statusChange = "farther"
			
			else:
    				
				xAxis = []

				blur1 = blur2

				rawCapture2.truncate(0)

				# Frame counter checks and updates

				if frameCount >= maxFrames:

					break

				frameCount += 1
				
				continue
			
			print("Status change: " + statusChange)

			# Writing to the data file
			
			if statusChange == "closer":

				fileName = "info/" + str(int(time.time())) + "_c" + "_0.4" ### CHANGE THIS HARDCODED VALUE!!!

				open(fileName, "w").close()

			elif statusChange == "farther":

				fileName = "info/" + str(int(time.time())) + "_f" + "_0.4" ### CHANGE THIS HARDCODED VALUE!!!
				
				open(fileName, "w").close()

		xAxis = []

	blur1 = blur2

	rawCapture2.truncate(0)

	# Frame counter checks and updates

	if frameCount >= maxFrames:

		break

	frameCount += 1

# Preparing the data and adding it to the debug file

xAxis = []
	
for i in range(0, len(actualDiffList)):

	xAxis.append(i)

for i in range(0, len(actualDiffList)):

	rawFile.write(str(xAxis[i]) + ", " + str(actualDiffList[i]) +  "\n")

xAxis = []

for i in range(0, len(filteredDiffList)):

	xAxis.append(i)

for i in range(0, len(filteredDiffList)):

	filteredFile.write(str(xAxis[i]) + ", " + str(filteredDiffList[i]) +  "\n")
