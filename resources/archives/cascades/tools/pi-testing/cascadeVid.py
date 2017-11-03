from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys

testingCascade = cv2.CascadeClassifier(sys.argv[1])

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size = (320, 240))

time.sleep(0.1)

minSize = int(sys.argv[2])
maxSize = int(sys.argv[3])

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if minSize == 0 and maxSize == 0:
        
        testObjects = testingCascade.detectMultiScale(gray)
    
    else:
        
        testObjects = testingCascade.detectMultiScale(gray, minSize=(minSize, minSize), maxSize=(maxSize, maxSize))
    
    for (x, y, w, h) in testObjects:
        
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow("Video", img)

    k = cv2.waitKey(1) & 0xff
    
    if k == 27:
        
        break

    rawCapture.truncate(0)

camera.close()
cv2.destroyAllWindows()