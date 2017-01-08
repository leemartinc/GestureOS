from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size = (640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        roiGray = gray[y:y+h, x:x+w]
        roiColor = img[y:y+h, x:x+w]
        
        eyes = eyeCascade.detectMultiScale(roiGray)
        
        for (ex, ey, ew, eh) in eyes:
            
            cv2.rectangle(roiColor, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow("Video", img)

    k = cv2.waitKey(1) & 0xff
    
    if k == 27:
        
        break
    
    rawCapture.truncate(0)

camera.close()
cv2.destroyAllWindows()
