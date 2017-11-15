import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import numpy as np

def nothing(x):
    pass

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
    learning = float(cv2.getTrackbarPos('backgroundRatio', 'mask') / 100)

    image = frame.array

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = fgbg.apply(image_gray)

    activeLocations = np.nonzero(mask)

    cv2.imshow('mask', mask)
    cv2.imshow('frame', activeLocations)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
