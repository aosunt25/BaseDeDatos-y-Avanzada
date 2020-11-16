from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.proyecto_final

collection = db['movie']

country =input()
myquery = [
{"$group": {"_id": "$country","total": {"$sum": 1}}},
{"$match" :{ "_id":country}}
]


# myquery = [
# {"$match": {"type":"TV Show"}},
# {"$group": {"_id": "$release_year","total": {"$sum": 1}}},
# {"$match" :{ "_id":"2017"}}
# ]
cursos = list(collection.aggregate(myquery))

for doc in cursos:
    print(doc["total"])
