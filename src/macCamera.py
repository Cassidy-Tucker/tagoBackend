import cv2
import numpy as np
import time
from zones import Zone
import uploadData

def nothing(x):
    pass

saveImage = False
imageNumber = 0

zones = [Zone('newZone')]

uploadData.createDomain("Test Domain", "it's in a room on the north side")
uploadData.createZone(zones)

cap = cv2.VideoCapture(0)
_, frame = cap.read()
w, h, _ = frame.shape

fgbg = cv2.createBackgroundSubtractorMOG2()

time.sleep(0.1)

# window setup
cv2.namedWindow('frame')
cv2.namedWindow('heatMap')

cv2.createTrackbar('Subtract', 'heatMap', 1, 100, nothing)
cv2.createTrackbar('Off-On', 'frame', 0, 1, nothing)
# setup callbacks
cv2.setMouseCallback('frame', zones[0].setSquare)

heatMap = np.zeros((w/2, h/2), dtype=np.uint8)

while True:
    record_data = cv2.getTrackbarPos('Off-On', 'frame')
    _, frame = cap.read()
    w, h, _ = frame.shape
    frame = cv2.resize(frame, (h/2,w/2))

    subValue = float(cv2.getTrackbarPos('Subtract', 'heatMap') / 100)

    subtract = np.full((w/2, h/2), subValue, dtype=np.uint8)

    mask = fgbg.apply(frame)

    heatMap = cv2.addWeighted(heatMap, .995, mask, .005, 0);

    if zones[0].rectReady == True:
        frame = zones[0].drawSquare(frame)

    while time.localtime().tm_sec % 5 == 0:
        if saveImage == True:
            uploadData.updateZoneInstance(zones, frame)
            uploadData.updateHeatmapInstance(frame)
            saveImage = False
            print "dataUploaded"

    saveImage = True

    cv2.imshow('frame', frame)
    cv2.imshow('heatMap', heatMap)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
