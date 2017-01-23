from transfunction import transfunction
from screenres import screenres
import cv2
import sys

w = screenres.width
h = screenres.height

xc = float(sys.argv[1])
yc = float(sys.argv[2])

def zoomIn(img):

    height, width = img.shape[:2]

    roi = img[int(round(height * 0.25)):int(round(height * 0.75)), int(round(width * 0.25)):int(round(width * 0.75))]
    
    return roi
 
def showImage():

  rawImg = cv2.imread("image.jpg")

  pipe = open("statusChange", "r")

  output = pipe.read()

  if output == "closer":

    img = zoomIn(rawImg)

  else:

    img = rawImg
  
  rawLoadImg = transfunction.transform(img, w, h, xc, yc)

  loadImg = cv2.resize(rawLoadImg, (w, h))

  cv2.imshow("window", loadImg)
  cv2.waitKey(1)

  key = cv2.waitKey(1) & 0xFF

  if key == 27:
    
    exit()

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:

  showImage()
    
 
