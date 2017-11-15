import cv2

x1,y1 = -1, -1
x2,y2 = -1, -1
drawing, rectReady = False, False

def setSquare(event, x, y, flags, params):
    global x1, y1, x2, y2, rectReady, drawing

    print event
    if event == cv2.EVENT_LBUTTONDOWN:
        rectReady = False
        drawing = True
        x1 = x
        y1 = y
        print "left mouse button down: " + str(x1) + " " + str(y1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            rectReady = True
            x2 = x
            y2 = y
            print "Mouse Move: " + str(x2) + " " + str(y2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False;
        rectReady = True
        x2 = x
        y2 = y
        print "Mouse Up: " + str(x2) + " " + str(y2)

def drawSquare(frame):
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), thickness=2)
    return frame
