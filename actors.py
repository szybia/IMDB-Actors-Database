from pymongo import MongoClient
import json


#   Connect to MongoDB localhost
client = MongoClient()

#   Use db
db = client['db']

#   Select collection
credits = db.credits

#   Delete existing actors collection
db.actors.drop()

#   Get all movie credits with cast
credits         = credits.find({}, {"movie_id": 1, "cast": 1, "_id":0})

#   Get number of documents in collection for looping
credits_count   = credits.count()

#   List to store actor dictionarys with movie information
actors      = []

#   Dictionary to pair actor_id with index in list for appending movies
actorNum    = {}

#   Iterate through each movie
for i in range(credits_count):

    #   cast        =   JSON document of all actors in movie
    #   movie_id    =   Movie_id to find in movies collection
    #   movie       =   All information about movie

    cast        =   json.loads(credits[i]['cast'])
    movie_id    =   credits[i]['movie_id']
    movie       =   db.movies.find({"id":movie_id})[0]

    #   Iterate through each cast member
    for j in range(len(cast)):

        cast_id     = cast[j]['id']
        cast_name   = cast[j]['name']

        #   If cast member already exists add movie to their list

        if cast_id in actorNum:
            actors[actorNum[cast_id]]['movies'].append(movie)
        else:
            actors.append({'actor_id': cast_id, 'name': cast_name, 'movies': [movie]})
            actorNum[cast_id] = len(actors)-1


#   Insert actors into Mongo
actorCount = db.actors.insert(actors)
print("Successfully imported {} documents into actorMovie.".format(len(actorCount)))
