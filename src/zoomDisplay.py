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
import cv2
import sys
import os

w = screenres.width
h = screenres.height

xc = float(sys.argv[1])
yc = float(sys.argv[2])

getImg = cv2.imread("image.jpg")

rawImg = cv2.resize(getImg, (w, h))

def zoomIn(img):

    height, width = img.shape[:2]

    rawRoi = img[int(round(height * 0.25)):int(round(height * 0.75)), int(round(width * 0.25)):int(round(width * 0.75))]

    roi = cv2.resize(rawRoi, (w, h))
    
    return roi
 
def showImage():

  fileList = os.listdir("info")

  if len(fileList) == 0:

    return

  for file in fileList:

    os.remove("info/" + file)

  fileList.sort()

  file = fileList[-1]

  fileName = file.split("_")

  output = fileName[1]

  if output == "f":

    img = zoomIn(rawImg)

  else:

    img = rawImg
  
  loadImg = transfunction.transform(img, w, h, xc, yc)

  cv2.imshow("window", loadImg)
  cv2.waitKey(1)

  key = cv2.waitKey(1) & 0xFF

  if key == 27:
    
    exit()

cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

loadImg = transfunction.transform(rawImg, w, h, xc, yc)

cv2.imshow("window", loadImg)
cv2.waitKey(1)

cv2.imshow("window", loadImg)
cv2.waitKey(1)

while True:

  showImage()
  