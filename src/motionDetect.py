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

#--- Adjustable Parameters ---#

imgSize= 256

blurRegion = 5

pixelThreshold = 10

dataSampleSize = 10

framesToIgnore = 10

lowerOutlierLimit = 25
upperOutlierCutOff = 150

xDataThreshold = 0.5
yDataThreshold = int(0.25 * imgSize)

zoomFactor = 0.4

frameCount = 0

frameCountLimit = int(input("Enter a frame count limit: "))

# Initializing lists

xData = []
xDataSample = []
xDataFiltered = []

yData = []
yDataSample = []

# Camera settings
camera = PiCamera()
camera.resolution = (imgSize,imgSize)
rawCapture1 = PiRGBArray(camera, size = camera.resolution)
rawCapture2 = PiRGBArray(camera, size = camera.resolution)

time.sleep(0.1)

# Capturing and processing the first frame
camera.capture(rawCapture1, format = "bgr", use_video_port = True)
rawFrame1 = rawCapture1.array

grayFrame1 = cv2.cvtColor(rawFrame1, cv2.COLOR_BGR2GRAY)
blurFrame1 = cv2.GaussianBlur(grayFrame1, (blurRegion, blurRegion), 0)

rawCapture1.truncate(0)
	
while True:

	# Incrementing the frame count and checking for valid count
	frameCount += 1

	if frameCount <= ignore:

		continue

	if frameCount > frameCountLimit:

		break

	# Capturing and processing another frame
	camera.capture(rawCapture2, format = "bgr", use_video_port = True)
	rawFrame2 = rawCapture2.array

	grayFrame2 = cv2.cvtColor(rawFrame2, cv2.COLOR_BGR2GRAY)
	blurFrame2 = cv2.GaussianBlur(grayFrame2, (blurRegion, blurRegion), 0)
	diffImg = cv2.absdiff(blurFrame1, blurFrame2)
	threshImg = cv2.threshold(diffImg, pixelThreshold, 255, cv2.THRESH_BINARY)[1]

	# Finding white points, calculating their difference/maximum, and adding the values
	whitePoints = cv2.findNonZero(threshImg)

	if whitePoints is not None:

		whitePoints = cv2.findNonZero(threshImg).tolist()

		whitePointXValues = []
		whitePointYValues = []

		for doubleList in whitePoints:

			for list in doubleList:

				whitePointXValues.append(list[0])
				whitePointYValues.append(list[1])

		xMinimum = min(whitePointXValues)
		xMaximum = max(whitePointXValues)
		xDifference = xMaximum - xMinimum
		
		yMinimum = min(whitePointYValues)
		yMaximum = max(whitePointYValues)
		yDifference = yMaximum - yMinimum

		xData.append(xDifference)
		yData.append(yDifference)

	else:

		xData.append(0)
		yData.append(0)

	# Analyzing the data gathered
	if len(xData) % dataSampleSize == 0:

		# Determining the windows of data
		xDataSample = xData[len(xData) - dataSampleSize : len(xData)]
		yDataSample = yData[len(yData) - dataSampleSize : len(yData)]

		xSampleFiltered = []
		ySampleFiltered = []

		# Filtering the window of data
		for i in range(0, len(xDataSample)):

			if xDataSample[i] > lowerOutlierLimit and xDataSample[i] < upperOutlierLimit:

				xDataFiltered.append(xDataSample[i])

				xSampleFiltered.append(xDataSample[i])
				ySampleFiltered.append(yDataSample[i])
		
		if len(xSampleFiltered) >= 2:
			
			maxIndex = xSampleFiltered.index(max(xSampleFiltered))
			
			if maxIndex == 0:

				minIndex = 0
			
			else:

				minIndex = xSampleFiltered.index(min(xSampleFiltered)) - 1

			xSampleFiltered.remove(max(xSampleFiltered))
			xSampleFiltered.remove(min(xSampleFiltered))

			del ySampleFiltered[maxIndex]
			del ySampleFiltered[minIndex]

		# Ignoring the data if too little
		if len(xSampleFiltered) <= 1:

			blurFrame1 = blurFrame2
			rawCapture2.truncate(0)
			
			continue

		# Creating an x-axis for the linear regression
		xAxis = []

		for i in range(1, len(xSampleFiltered) + 1):

			xAxis.append(i)
		
		# Finding the slope of the linear regression if possible
		if len(xSampleFiltered) > 0:
		
			slope = numpy.polyfit(xAxis, xSampleFiltered, 1)[0]

		# Finding the difference between the maximum and minimum y value
		yData = max(ySampleFiltered) - min(ySampleFiltered)

		print(yData)

		# Making a decision based on the data values
		if yData > yDataThreshold:

			gestureDetected = "reset"

		elif len(xSampleFiltered) > 0:

			if slope < -xDataThreshold:

				gestureDetected = "closer"
			
			elif slope > xDataThreshold:

				gestureDetected = "farther"

			else:

				blurFrame1 = blurFrame2
				rawCapture2.truncate(0)

				continue
		
		else:
			
			print("[ERROR] Decision not possible!")
			
		# Printing out the decision
		print("[INFO] Gesture detected: " + gestureDetected)

		# Passing the decision through the pipe
		if gestureDetected == "reset":

			fileName = "info/" + str(int(time.time())) + "_r" + "_" + str(zoomFactor)

			open(fileName, "w").close()
			
		if gestureDetected == "closer":

			fileName = "info/" + str(int(time.time())) + "_c" + "_" + str(zoomFactor)

			open(fileName, "w").close()

		elif gestureDetected == "farther":

			fileName = "info/" + str(int(time.time())) + "_f" + "_" + str(zoomFactor)
			
			open(fileName, "w").close()

	blurFrame1 = blurFrame2
	rawCapture2.truncate(0)
		
# Opening the data files
xDataFile = open("data-raw.csv", "w")
xDataFilteredFile = open("data-filtered.csv", "w")
yDataFile = open("data-y.csv", "w")

# Writing the raw x data file
xAxis = []
	
for i in range(0, len(xData)):

	xAxis.append(i)

for i in range(0, len(xData)):

	xDataFile.write(str(xAxis[i]) + ", " + str(xData[i]) +  "\n")

# Writing the filtered x data file
xAxis = []

for i in range(0, len(xDataFiltered)):

	xAxis.append(i)

for i in range(0, len(xDataFiltered)):

	xDataFilteredFile.write(str(xAxis[i]) + ", " + str(xDataFiltered[i]) +  "\n")

# Writing the y data file
xAxis = []

for i in range(0, len(yData)):

	xAxis.append(i)

for i in range(0, len(yData)):

	yDataFile.write(str(xAxis[i]) + ", " + str(yData[i]) + "\n")
