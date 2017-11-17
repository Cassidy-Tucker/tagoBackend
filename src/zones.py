import cv2

class Zone:
    def __init__(self):
	self.name = 'Zone1'
        self.x = -1
        self.y = -1
        self.width = -1
        self.height = -1
        self.drawing = False
        self.rectReady = False

    def setSquare(self, event, x, y, flags, params):
        print event
        if event == cv2.EVENT_LBUTTONDOWN:
            self.rectReady = False
            self.drawing = True
            self.x = x
            self.y = y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                self.rectReady = True
                self.width = x - self.x
                self.height = y - self.y
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False;
            self.rectReady = True
            self.width = x - self.x
            self.height = y - self.y

    def drawSquare(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), (0,0,255), thickness=2)
	cv2.putText(frame, 'Zone: ' + self.name, (self.x + 20, self.y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
        return frame

    def getRoiValue(self, frame):
        frame = frame[self.y : self.y + self.height, self.x : self.x + self.width]
	frameMean = cv2.mean(frame)
	return frameMean
