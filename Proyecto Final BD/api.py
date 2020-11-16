import redis

from pymongo import MongoClient
from bson.objectid import ObjectId

#Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.proyecto_final
collection = db['movie']

#Connection to redis DB
r = redis.Redis(host="localhost", port=6379, db=0)

#def movieName(movie):

#def actorName(actor):

#def tvShowName(tvShow):

def totalNumMovTV():
    try:
        total = r.get("TotalMovies").decode("utf-8")
        print("Redis")
        print("Total number of movies ", total)
    except:
        print("Mongo")
        cursos = collection.count()
        r.set("TotalMovies",cursos)
        print("Total number of movies ", cursos)
   


def totalMovCountry(country):
    try:
        total = r.get(country).decode("utf-8")
        print("Redis")
        print("Total number of movies on ", country, " is ", total)
    except:
        print("Mongo")
        myquery = [
        {"$group": {"_id": "$country","total": {"$sum": 1}}},
        {"$match" :{ "_id":country}}
        ]
        cursos = list(collection.aggregate(myquery))
        for doc in cursos:
            r.set(country, doc["total"])
            print("Total number of movies on ", country, " is ", doc["total"])

def totalMovieTVperYear(year):
    myquery = [
    {"$match": {"type":"TV Show"}},
    {"$group": {"_id": "$release_year","total": {"$sum": 1}}},
    {"$match" :{ "_id":year}} 
    ]
    cursos = list(collection.aggregate(myquery))

#def addMovie():

#def addTVShow():


menu = 0

while menu!= 9:
    print('Menu del Api \n')
    print('1. Give movie name \n')
    print('2. Give actor name \n')
    print('3. Give a TV show name \n')
    print('4. Total number of movies and TV shows \n')
    print('5. Total number of movies for a given country \n')
    print('6. Total number of TV shows for a given release year \n')
    print('7. Add new movie \n')
    print('8. Add a new TV show \n')
    print('9. Exit')
    menu = int(input())
    if menu == 1:
        print("C")
    elif menu == 5:
        country = input("Name of the country\n")
        totalMovCountry(country)
