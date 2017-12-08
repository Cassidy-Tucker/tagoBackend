import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
from tago import *

def nothing(x):
    pass

def setSelectedZone(zone):
    global selected_zone
    selected_zone = zone

# setup variables
imageNumber = 1
saveImage = True
zones = [Zone('zone1'),Zone('zone2'),Zone('zone3')]
base_image_capture = True
selected_zone = 0
record_data = 0

createDomain("TestArea", "it's in a room on the north side")
createZone(zones)

# setup camera
camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 30
camera.iso = 1600
rawCapture = PiRGBArray(camera)

time.sleep(0.5)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

# setup background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history=2500)

# setup window
cv2.namedWindow('image')
cv2.createTrackbar('selected zone', 'image', 0, 2, setSelectedZone)
cv2.createTrackbar('Off-On', 'image', 0, 1, nothing)

# setup blank heatmap
heatMap = np.zeros((480, 640), dtype=np.uint8)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    cv2.setMouseCallback('image', zones[selected_zone].setSquare)

    record_data = cv2.getTrackbarPos('Off-On', 'image')

    if base_image_capture:
        base_image = frame.array
        base_image_capture = False

    image = np.array((480, 640), np.uint8)
    image = np.copy(frame.array)

    diff = getDiff(base_image, image)
    diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    mask = fgbg.apply(diff)

    heatMap = cv2.addWeighted(heatMap, 0.97, mask, 0.03, 0)

    heatMap_color = cv2.applyColorMap(heatMap, cv2.COLORMAP_JET)

    for zone in zones:
        if zone.rectReady == True:
            image = zone.drawSquare(image)
            heatMap_color = zone.drawSquare(heatMap_color)

    while time.localtime().tm_sec % 5 == 0:
        if saveImage == True & record_data == 1:
            updateZoneInstance(zones, heatMap)
            updateHeatmapInstance(heatMap_color)
            saveImage = False
            print "dataUploaded"
    saveImage = True
    
    if record_data == 1:
        cv2.circle(image, (640-60, 50), 10, (0, 0, 255), -1)
        cv2.putText(image, "RECORDING", (640 - 110, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        
    cv2.putText(image, "Selected Zone: Zone" + str(selected_zone), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    cv2.putText(image, "Press P to take a new base image", (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    cv2.imshow('diff', diff)
    cv2.imshow('image', image)
    cv2.imshow('base_image', base_image)
    cv2.imshow('heatmap', heatMap_color)

    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('p'):
        base_image = frame.array
        # base_image = cv2.GaussianBlur(base_image, (17, 17), 0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
