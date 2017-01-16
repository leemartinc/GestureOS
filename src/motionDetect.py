from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2

camera = PiCamera()
camera.resolution = (1280,960)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(1280,960))

print("[INFO] warming up...")

time.sleep(1)
avg = None
motionCounter = 0

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
	frame = f.array
	timestamp = datetime.datetime.now()
	text = "No motion in progress!"
 
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	if avg is None:
                
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		
		print("[INFO] All ready!")

		continue
 
	cv2.accumulateWeighted(gray, avg, 0.75) # Adjust this value (update speed, contributes to sensitivity)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1] # More research needed...
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # More research needed...
 
	for c in contours:

		if cv2.contourArea(c) < 5000: # More research needed...
                        
			continue

		print("[INFO] Hand gesture detected!")
		exit()
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Motion in progress!"
 
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, "[Motion Status]: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
	
	cv2.imshow("Video Feed", frame)
	key = cv2.waitKey(1) & 0xFF
 
	if key == 27:
                
		break
 
	rawCapture.truncate(0)
