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
import numpy
import time
import cv2

### CUSTOMIZABLE VARIABLES ###

imgSize= 256
blurSize = 5
threshold = 10

sampleSize = 10
lowerOutlierCutOff = 25
upperOutlierCutOff = 150

epsilon = 0.5

zoomFactor = 0.4

#----------------------------#

# Initializing lists
xAxis = []
actualDiffList = []
filteredDiffList = []
windowOfData = []
filteredWindowOfData = []

# Camera settings
camera = PiCamera()
camera.resolution = (imgSize,imgSize)
rawCapture1 = PiRGBArray(camera, size = camera.resolution)
rawCapture2 = PiRGBArray(camera, size = camera.resolution)

time.sleep(0.1)

# Capturing the first frame
camera.capture(rawCapture1, format = "bgr", use_video_port = True)
frame1 = rawCapture1.array
gray1= cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
blur1 = cv2.GaussianBlur(gray1, (blurSize, blurSize), 0)

rawCapture1.truncate(0)

while True:

	# Capturing and processing a frame
	camera.capture(rawCapture2, format = "bgr", use_video_port = True)
	frame2 = rawCapture2.array

	gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
	blur2 = cv2.GaussianBlur(gray2, (blurSize, blurSize), 0)
	diffImg = cv2.absdiff(blur1, blur2)
	thresh = cv2.threshold(diffImg, threshold, 255, cv2.THRESH_BINARY)[1]

	# Finding white points, calculating their difference, and adding the value
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

	# Analyzing the data gathered
	if len(actualDiffList) % sampleSize == 0:

		# Determining the window of data
		windowOfData = actualDiffList[len(actualDiffList) - sampleSize : len(actualDiffList)]
		filteredWindowOfData = []

		# Filtering the window of data
		for item in windowOfData:

			if item > lowerOutlierCutOff and item < upperOutlierCutOff:

				filteredWindowOfData.append(item)
				filteredDiffList.append(item)
		
		if len(filteredWindowOfData) >= 2:
    			
			filteredWindowOfData.remove(max(filteredWindowOfData))
			filteredWindowOfData.remove(min(filteredWindowOfData))

		# Ignoring the data if too little
		if len(filteredWindowOfData) <= 1:

			blur1 = blur2
			rawCapture2.truncate(0)
			
			continue

		# Creating an x-axis for the linear regression
		for i in range(1, len(filteredWindowOfData) + 1):

			xAxis.append(i)
		
		# Finding the slope of the linear regression if possible
		if len(filteredWindowOfData) > 0:
		
			slope = numpy.polyfit(xAxis, filteredWindowOfData, 1)[0]

			# Making a decision based on the slope's value
			if slope < -epsilon:

				statusChange = "closer"
			
			elif slope > epsilon:

				statusChange = "farther"

			else:
    				
				xAxis = []
				blur1 = blur2
				rawCapture2.truncate(0)

				continue
			
			# DEBUG: Printing out the decision
			print("[INFO] Gesture detected: " + statusChange)

			# Passing the decision through the pipe
			if statusChange == "closer":

				fileName = "info/" + str(int(time.time())) + "_c" + "_" + str(zoomFactor)

				open(fileName, "w").close()

			elif statusChange == "farther":

				fileName = "info/" + str(int(time.time())) + "_f" + "_" + str(zoomFactor)
				
				open(fileName, "w").close()

		# Reseting variables for the next iteration
		xAxis = []

	blur1 = blur2
	rawCapture2.truncate(0)

	# Exit the loop if Esc pressed
	key = cv2.waitKey(1) & 0xFF
	
	if key == 27:
		
		break
		
# Opening the data files
rawFile = open("data-raw.csv", "w")
filteredFile = open("data-filtered.csv", "w")

# Writing the raw data file
xAxis = []
	
for i in range(0, len(actualDiffList)):

	xAxis.append(i)

for i in range(0, len(actualDiffList)):

	rawFile.write(str(xAxis[i]) + ", " + str(actualDiffList[i]) +  "\n")

# Writing the filtered data file
xAxis = []

for i in range(0, len(filteredDiffList)):

	xAxis.append(i)

for i in range(0, len(filteredDiffList)):

	filteredFile.write(str(xAxis[i]) + ", " + str(filteredDiffList[i]) +  "\n")
