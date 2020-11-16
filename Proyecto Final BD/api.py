import redis

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.proyecto_final
collection = db['movie']

def movieName(movie):

def actorName(actor):

def tvShowName(tvShow):

def totalNumMovTV():
    cursos = collection.count()


def totalMovCountry(country):
    myquery = [
    {"$group": {"_id": "$country","total": {"$sum": 1}}},
    {"$match" :{ "_id":country}}
    ]
    cursos = list(collection.aggregate(myquery))

def totalMovieTVperYear(year):
    myquery = [
    {"$match": {"type":"TV Show"}},
    {"$group": {"_id": "$release_year","total": {"$sum": 1}}},
    {"$match" :{ "_id":year}} 
    ]
    cursos = list(collection.aggregate(myquery))

def addMovie():

def addTVShow():


menu = 0
while menu!= 6:
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
    if menu == 1:
