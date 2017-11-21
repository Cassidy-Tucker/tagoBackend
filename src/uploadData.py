from pymongo import MongoClient
import bson
from datetime import datetime
import time
import cv2
import base64

client = MongoClient('mongodb://Matt:skool16@ds113626.mlab.com:13626/tago_areas')
db = client.tago_areas

collections = {
    "areas": db.areas,
    "zones": db.zones,
    "heatmaps": db.heatmaps
}

def createArea(name, description):
    global areaId

    areaId = collections['areas'].insert_one(
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
                "area" : areaId,
                "intervals" : [],
                "dateCreated" : getCurrentTime()
            }
        ).inserted_id

        collections['areas'].find_one_and_update(
            {"_id" : areaId},
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
            { "area" : areaId , "name" : zone.name },
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
            "area" : areaId
        }
    ).inserted_id

    collections['areas'].find_one_and_update(
        { "_id" : areaId },
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
