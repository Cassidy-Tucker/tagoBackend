import cv2
import numpy as np
from pymongo import MongoClient
import bson
from datetime import datetime
import time
import base64

client = MongoClient('mongodb://Matt:skool16@ds113826.mlab.com:13826/tago')
db = client.tago

collections = {
    "domains": db.domains,
    "zones": db.zones,
    "heatmaps": db.heatmaps
}

def getCurrentTime():
    currentTime = datetime.utcnow()
    return int(time.mktime(currentTime.timetuple())) * 1000

def saveImage(heatmap):
    cv2.imwrite('./public/img/heatmap.png', heatmap)

def getDiff(base_image, current_image):
    # base_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    # current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    base_image = cv2.GaussianBlur(base_image, (17, 17), 0)
    current_image = cv2.GaussianBlur(current_image, (17, 17), 0)

    diff = cv2.absdiff(base_image, current_image)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    return diff

def createDomain(name, description):
    global domainId

    domainId = collections['domains'].insert_one(
        {
            "name" : name,
            "description" : description,
            "heatmaps" : [],
            "zones" : [],
            "dateCreated" : getCurrentTime()
        }
    ).inserted_id

def createZone(zones):
    for zone in zones:
        zoneId = collections['zones'].insert_one(
            {
                "name" : zone.name,
                "domain" : domainId,
                "intervals" : [],
                "dateCreated" : getCurrentTime()
            }
        ).inserted_id

        collections['domains'].find_one_and_update(
            {"_id" : domainId},
            {"$push" :
                {"zones" :
                    {
                        "name" : zone.name,
                        "zoneId" : zoneId
                    }
                }
            }
        )

def updateZoneInstance(zones, frame):
    for zone in zones:
        collections['zones'].find_one_and_update(
            { "domain" : domainId , "name" : zone.name },
            { "$push" :
                {"intervals" :
                    {
                        "activity" : zone.getRoiValue(frame),
                        "dateCreated" : getCurrentTime()
                    }
                }
            }
        )

def updateHeatmapInstance(heatmap):
    saveImage(heatmap)
    data = open('./public/img/heatmap.png')
    data = base64.b64encode(data.read())

    heatmapId = collections['heatmaps'].insert_one(
        {
            "dateCreated" : getCurrentTime(),
            "image" : data,
            "domain" : domainId
        }
    ).inserted_id

    collections['domains'].find_one_and_update(
        { "_id" : domainId },
        { "$push" :
            {"heatmaps" :
                {
                    "dateCreated" : getCurrentTime(),
                    "id" : heatmapId
                }
            }
        }
    )

class Zone:
    def __init__(self, name):
	self.name = name
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
        frameMean = round(cv2.mean(frame)[0] / 255, 2)
        print frameMean
        return frameMean
