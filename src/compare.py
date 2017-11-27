import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time

first_cap = True

# setup camera
camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 30
camera.iso = 400 
rawCapture = PiRGBArray(camera)

time.sleep(0.5)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

time.sleep(0.5)

fgbg = cv2.createBackgroundSubtractorMOG2(history=1000)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    if first_cap:    
        space = frame.array
        space = cv2.GaussianBlur(space, (9,9), 0)
        space_gray = cv2.cvtColor(space, cv2.COLOR_BGR2GRAY)
        first_cap = False

    image = frame.array
    image = cv2.GaussianBlur(image, (9, 9), 0)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(space_gray, image_gray)

    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    
    mask = fgbg.apply(mask)

    cv2.imshow('mask', mask)
    cv2.imshow('diff', diff)
    cv2.imshow('image', image)
    cv2.imshow('space', space)

    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
