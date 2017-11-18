from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)

db = client.tago
areas = db.areas

dbArea = {
    "name" : "test Area",
    "description" : "Test area for mongo uplaods",
    "zones" : [],
    "heatMap" : []
}

areaId = areas.insert_one(dbArea).inserted_id

print areaId
