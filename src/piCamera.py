import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
from zones import Zone
import uploadData
from compare import getDiff

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

uploadData.createDomain("TestArea", "it's in a room on the north side")
uploadData.createZone(zones)

# setup camera
camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 32
camera.iso = 800 
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
camera.brightness = 75

# setup background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history=1000)

# setup window
cv2.namedWindow('image')
cv2.setMouseCallback('image', zones[cv2.getTrackbarPos('selected zone', 'image')].setSquare)
cv2.createTrackbar('selected zone', 'image', 0, 2, setSelectedZone)

# setup blank heatmap
heatMap = np.zeros((480, 640), dtype=np.uint8)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    print 'Zone: ' + str(selected_zone)
    if base_image_capture:
        base_image = frame.array
        base_image_capture = False

    image = frame.array
    
    diff = getDiff(base_image, image)

    mask = fgbg.apply(diff)

    heatMap = cv2.addWeighted(heatMap, 0.97, mask, 0.03, 0)

    heatMap_color = cv2.applyColorMap(heatMap, cv2.COLORMAP_JET)

    for zone in zones:
        if zone.rectReady == True:
            image = zone.drawSquare(image)
    
    cv2.putText(image, "Selected Zone: Zone" + str(selected_zone), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    while time.localtime().tm_sec % 5 == 0:
        if saveImage == True:
            uploadData.updateZoneInstance(zones, heatMap)
            uploadData.updateHeatmapInstance(heatMap_color)
            saveImage = False
            print "dataUploaded"

    saveImage = True

    cv2.imshow('diff', diff)
    cv2.imshow('image', image)
    cv2.imshow('mask', mask)
    cv2.imshow('heatmap', heatMap_color)

    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
