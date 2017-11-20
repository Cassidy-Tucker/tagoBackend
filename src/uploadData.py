from pymongo import MongoClient
from datetime import datetime
import time

client = MongoClient('localhost', 27017)
db = client.tago

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
    heatmapId = collections['heatmaps'].insert_one(
        {
            "dateCreated" : getCurrentTime(),
            "binaryVal" : heatmap,
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

def getCurrentTime():
    currentTime = datetime.utcnow()
    return int(time.mktime(currentTime.timetuple())) * 1000
