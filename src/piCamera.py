import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np

camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)

fgbg = cv2.createBackgroundSubtractorMOG2()

heatMap = numpy.zeros((640, 480), dtype=np.uint8)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    image = frame.array

    mask = fgbg.apply(image)

    heatMap = cv2.addWeighted(heatMap, .995, mask, .005, 0)

    cv2.imshow('Heatmap', heatMap)
    cv2.imshow('Frame', mask)

    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
