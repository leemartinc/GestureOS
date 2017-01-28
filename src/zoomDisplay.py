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

zoomFactor = 0.25

rawImg = cv2.imread("image.jpg")

img = cv2.resize(rawImg, (w, h))

orgImg = img.copy()

def zoomOut(img, depth):

  height, width = img.shape[:2]

  depth -= 1

  if depth == 0:

    return img

  for i in range(0, depth):

    img = zoomIn(img)
  
  roi = cv2.resize(img, (w, h))

  return roi

def zoomIn(img):

  height, width = img.shape[:2]

  rawRoi = img[int(round(height * zoomFactor)):int(round(height * (1 - zoomFactor))), int(round(width * zoomFactor)):int(round(width * (1 - zoomFactor)))]

  roi = cv2.resize(rawRoi, (w, h))
    
  return roi

def getCommand():

  fileList = os.listdir("info")

  if len(fileList) == 0:

    return None

  for file in fileList:

    os.remove("info/" + file)

  fileList.sort()

  file = fileList[-1]

  fileName = file.split("_")

  output = fileName[1]

  return output
 
def showImage(orgImg, img, command):

  if command == "f":

    for i in range(3, 0, -1):

      img = zoomOut(orgImg, i)

      loadImg = transfunction.transform(img, w, h, xc, yc)

      cv2.imshow("window", loadImg)
      cv2.waitKey(1)

      key = cv2.waitKey(1) & 0xFF

      if key == 27:
        
        exit()
      
      time.sleep(0.1)
    
    return img
  
  elif command == "c":
    
    for i in range(0, 3):

      img = zoomIn(img)

      loadImg = transfunction.transform(img, w, h, xc, yc)

      cv2.imshow("window", loadImg)
      cv2.waitKey(1)

      key = cv2.waitKey(1) & 0xFF

      if key == 27:
        
        exit()
      
      time.sleep(0.1)

    return img


cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

loadImg = transfunction.transform(img, w, h, xc, yc)

cv2.imshow("window", loadImg)
cv2.waitKey(1)

while True:

  command = getCommand()
  
  if command is None:

    continue

  img = showImage(orgImg, img, command)
  