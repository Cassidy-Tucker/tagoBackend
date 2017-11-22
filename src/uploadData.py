from pymongo import MongoClient
import bson
from datetime import datetime
import time
import cv2
import base64

client = MongoClient('mongodb://Matt:skool16@ds113826.mlab.com:13826/tago')
db = client.tago

collections = {
    "domains": db.domains,
    "zones": db.zones,
    "heatmaps": db.heatmaps
}

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
                        "date" : "testDate",
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
                {"id" : heatmapId}
            }
        }
    )

def saveImage(heatmap):
    cv2.imwrite('./public/img/heatmap.png', heatmap)

def getCurrentTime():
    currentTime = datetime.utcnow()
    return int(time.mktime(currentTime.timetuple())) * 1000
