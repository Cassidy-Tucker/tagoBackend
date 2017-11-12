import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    image = frame.array

    cv2.imshow('Frame', image)

    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
