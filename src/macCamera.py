import cv2
import numpy as np
import time
from zones import Zone

def nothing(x):
    pass

saveImage = False
imageNumber = 0
zone1 = Zone()

cap = cv2.VideoCapture(0)
_, frame = cap.read()
w, h, _ = frame.shape

fgbg = cv2.createBackgroundSubtractorMOG2()

time.sleep(0.1)

# window setup
cv2.namedWindow('frame')
cv2.namedWindow('heatMap')

cv2.createTrackbar('Subtract', 'heatMap', 1, 100, nothing)

# setup callbacks
cv2.setMouseCallback('frame', zone1.setSquare)

heatMap = np.zeros((w/2, h/2), dtype=np.uint8)

while True:
    _, frame = cap.read()
    w, h, _ = frame.shape
    frame = cv2.resize(frame, (h/2,w/2))

    subValue = float(cv2.getTrackbarPos('Subtract', 'heatMap') / 100)
    # frameNoiseReduction = cv2.fastNlMeansDenoisingColored(frame, None , 10, 10, 7, 21)
    subtract = np.full((w/2, h/2), subValue, dtype=np.uint8)

    mask = fgbg.apply(frame)

    heatMap = cv2.addWeighted(heatMap, .995, mask, .005, 0);
    # heatMap = heatMap - subtract

    if zone1.rectReady == True:
        frame = zone1.drawSquare(frame)

    while time.localtime().tm_sec % 5 == 0:
        if saveImage == True:
            # cv2.imwrite('./public/img/area' + str(imageNumber) + '.jpg', heatMap_color)
            zone1.getRoiValue(frame)
            saveImage = False
            imageNumber += 1
            print "Saved Image"

    saveImage = True

    cv2.imshow('frame', frame)
    cv2.imshow('heatMap', heatMap)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    if cv2.waitKey(1) & 0xff == ord('p'):
        print "image saved"
        cv2.imwrite('cap.jpg', heatMap)

cv2.destroyAllWindows()
cap.release()
