import redis

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import date

#Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.proyecto_final
collection = db['movie']


#Connection to redis DB
r = redis.Redis(host="localhost", port=6379, db=0)

#r.config_set("maxmemory", "10000")
#Información de contexto
now = date.today()

def movieName(movie):
    try:
        key = "1_"+movie
        text = r.get(key).decode("utf-8")
        print("Redis")
        print(text)
    except:
        print("Mongo")
        myquery = {"title" : movie}
        cursos = list(collection.find(myquery))
        
        for doc in cursos:
            if (doc["type"] == "Movie"):
                text = "director: " + doc["director"] +"\n" + "cast: " + doc["cast"] +"\n"+ "country: " + doc["country"] +"\n"+ "release_year: " + doc["release_year"] +"\n"
                key = "1_"+movie
                r.set(key, text)
                r.expire(key, "60")
                print(text)

def actorName(actor):
    try:
        key = "2_"+actor
        text = r.get(key).decode("utf-8")
        print("Redis")
        print(text)
    except:
        print("Mongo")
        text = ""
        key = "2_"+actor
        for doc in collection.find({}, {"cast": "Smita Malhotra"},{"title" : 1, "_id" : 0}):
            #text += doc["title"] +" "
            print(doc)
        print( text)
        #r.set(key, text)
        
        #r.expire(key, "60")

def tvShowName(tvShow):
    try:
        key = "3_"+tvShow
        text = r.get(key).decode("utf-8")
        print("Redis")
        print(text)
    except:
        print("Mongo")
        myquery = {"title" : tvShow}
        cursos = list(collection.find(myquery))
        for doc in cursos:
           if (doc["type"] == "TV Show"):
                text = "director: " + doc["director"] +"\n" + "cast: " + doc["cast"] +"\n"+ "country: " + doc["country"] +"\n"+ "release_year: " + doc["release_year"] +"\n"
                key = "3_"+tvShow
                r.set(key, text)
                r.expire(key, "60")
                print(text)

def totalNumMovTV():
    try:
        total = r.get("TotalMovies").decode("utf-8")
        print("Redis")
        print("Total number of movies ", total)
    except:
        print("Mongo")
        cursos = collection.count()
        r.set("TotalMovies",cursos)
        r.expire("TotalMovies", "60")
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
            r.expire(country, "60")
            print("Total number of movies on ", country, " is ", doc["total"])

def totalMovieTVperYear(year):
    try:
        total = r.get(year).decode("utf-8")
        print("Redis")
        print("The total TV Shows on ", year, " are ", total , end="\n")
    except:
        print("Mongo")
        myquery = [
        {"$match": {"type":"TV Show"}},
        {"$group": {"_id": "$release_year","total": {"$sum": 1}}},
        {"$match" :{ "_id":year}} 
        ]
        cursos = list(collection.aggregate(myquery))
       
        for doc in cursos:
            r.set(year, doc["total"])
            r.expire(year, "60")
            print("The total TV Shows on ", year," are ", doc["total"],  end="\n")

def addMovie(title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
    query = [
    {"$match" :{"title":title}}
    ]
    cursos = list(collection.aggregate(query))
    if(len(cursos) > 0):
        print("Error: The movie name already exists in the database.\n")
    else:
        query = {"type": "Movie", "title":title, "director":director, "cast":cast, "country":country, "date_added": date_added, "release_year": release_year, "rating": rating, "duration": duration, "listed_in": listed_in, "description": description}
        cursos = collection.insert_one(query)
        print("Movie \'", title, "\' was succesfully added to the database")

def addTVShow(title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
    query = [
    {"$match" :{"title":title}}
    ]
    cursos = list(collection.aggregate(query))
    if(len(cursos) > 0):
        print("Error: The TV Show name already exists in the database.\n")
    else:
        query = {"type": "TV Show", "title":title, "director":director, "cast":cast, "country":country, "date_added": date_added, "release_year": release_year, "rating": rating, "duration": duration, "listed_in": listed_in, "description": description}
        cursos = collection.insert_one(query)
        print("TV Show \'", title, "\' was succesfully added to the database")


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
        movie = input("Write the name of the movie\n")
        movieName(movie)
    elif menu == 2:
        actor = input("Write the name of the actor\n")
        actorName(actor)   
    elif menu == 3:
        tvShow = input("Write the name of the TV Show\n")
        tvShowName(tvShow)   
    elif menu == 4:
        totalNumMovTV()
    elif menu == 5:
        country = input("Name of the country\n")
        totalMovCountry(country)
    elif menu == 6:
        year = input("Write the year\n")
        totalMovieTVperYear(year)
    elif menu == 7:
        title = input("Name of the movie:\n")
        director = input("Director:\n")
        cast = input("Movie cast:\n")
        country = input("Name of the country:\n")
        date_added = now.strftime("%B %d, %Y")
        release_year = input("Release year:\n")
        rating = input("Rating:\n")
        duration = input("Duration:\n")
        listed_in = input("Listed in:\n")
        description = input("Description\n")
        addMovie(title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)
    elif menu == 8:
        title = input("Name of the movie:\n")
        director = input("Director:\n")
        cast = input("Movie cast:\n")
        country = input("Name of the country:\n")
        date_added = now.strftime("%B %d, %Y")
        release_year = input("Release year:\n")
        rating = input("Rating:\n")
        duration = input("Duration:\n")
        listed_in = input("Listed in:\n")
        description = input("Description\n")
        addTVShow(title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)


