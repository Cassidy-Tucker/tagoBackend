import cv2

def nothing(x):
    pass

def createOptionsWindow():
    cv2.namedWindow('Options')
    cv2.createTrackbar('On_Off', 'Options', 0, 1, nothing)

def getTrackbarPos():
    options = {
        "on" : cv2.getTrackbarPos('On_Off', "Options")
    }

    return options
