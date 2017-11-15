import cv2
import numpy as np
import time
import zones

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2()

_, frame = cap.read()
w, h, _ = frame.shape

time.sleep(0.1)

# window setup
cv2.namedWindow('frame')
cv2.namedWindow('heatMap')

cv2.createTrackbar('Subtract', 'heatMap', 1, 100, nothing)

# setup callbacks
cv2.setMouseCallback('frame', zones.setSquare)

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

    if zones.rectReady == True:
        frame = zones.drawSquare(frame)

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
