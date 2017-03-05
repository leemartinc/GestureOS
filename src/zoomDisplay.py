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
from transfunction import transfunction
from screenres import screenres
import time
import cv2
import sys
import os

w = screenres.width
h = screenres.height

xc = 0.3
yc = 0.8

numberOfStages = 2

rawImg = cv2.imread("image.jpg")

img = cv2.resize(rawImg, (w, h))

roiList = [img]

def zoomOut(stageNumber):

  roi = roiList[stageNumber - 1]

  return roi

def zoomIn(img, stageNumber, factor):
  
  if len(roiList) <= stageNumber:

    height, width = img.shape[:2]

    rawRoi = img[int(round(height * factor)):int(round(height * (1 - factor))), int(round(width * factor)):int(round(width * (1 - factor)))]

    roi = cv2.resize(rawRoi, (w, h))

    roiList.append(roi)

    return roi

  else:

    roi = roiList[stageNumber]

    return roi        
  
def getCommand():

  fileList = os.listdir("info")

  if len(fileList) == 0:

    return "none", "none"

  for file in fileList:

    os.remove("info/" + file)

  fileList.sort()

  file = fileList[-1]

  fileName = file.split("_")

  gesture = fileName[1]

  zoomFactor = float(fileName[2])

  if gesture == None:

    gesture = "none"

  if zoomFactor == None:

    zoomFactor = "none"

  return gesture, zoomFactor

def zoom(img, status, zoomFactor, numberOfStages):

  stageFactor = zoomFactor/numberOfStages

  if status == "c":

    for i in range(1, numberOfStages + 1):

      newImg = zoomIn(img, i, stageFactor)

      img = newImg

      loadImg = transfunction.transform(img, w, h, xc, yc)

      cv2.imshow("window", loadImg)

      cv2.waitKey(1)

    return img

  else:

    for i in range(numberOfStages, 0, -1):

      newImg = zoomOut(i)

      loadImg = transfunction.transform(newImg, w, h, xc, yc)

      cv2.imshow("window", loadImg)

      cv2.waitKey(1)

    return newImg
      
cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

loadImg = transfunction.transform(img, w, h, xc, yc)

cv2.imshow("window", loadImg)

cv2.waitKey(1000)

time.sleep(0.01)

while True:

  gesture, zoomFactor = getCommand()

  if gesture == "none" or zoomFactor == "none":

    continue

  key = cv2.waitKey(1) & 0xFF

  if key == 27:

    break
  
  img = zoom(img, gesture, zoomFactor, numberOfStages)
