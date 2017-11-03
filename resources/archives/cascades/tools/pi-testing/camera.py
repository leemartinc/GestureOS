from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size = (640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    
	image = frame.array

	cv2.imshow("Video", image)

	key = cv2.waitKey(1) & 0xFF

	if key == 27:
		
		break

	rawCapture.truncate(0)

camera.close()
cv2.destroyAllWindows()