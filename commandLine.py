from pymongo import MongoClient
import json
import pprint
import os

if __name__ == "__main__":
    os.system('clear')

    #   Connect to MongoDB localhost
    client = MongoClient()

    #   Use db
    db = client['db']


    choice     = int(raw_input("0   : All documents.\n1   : Actor movies.\n2   : Actors in order.\n3   : Number of movies actor has starred in.\n4   : Actors movie titles\n\nChoice: "))

    if choice == 0:
        os.system('clear')
        actorMovies = db.actors.find()
        size        = actorMovies.count()
        for i in range(size):
            pprint.pprint(actorMovies[i])
    elif choice == 1:
        os.system('clear')
        actorName      = raw_input("Please enter name of any actor : ")
        actorMovies = db.actors.find({"name":actorName}, {"_id":0, "name":0})
        actorMovies = actorMovies[0]['movies']
        pprint.pprint(actorMovies)
    elif choice == 2:
        os.system('clear')
        actorName      = raw_input("Ascending or descending order? (A/D)\n")
        if actorName == 'A':
            actorMovies = db.actors.find({}, {"_id":0, "actor_id":0 ,"movies":0}).sort([("name", 1)])
            for i in range(actorMovies.count()):
                print(actorMovies[i])
        else:
            actorMovies = db.actors.find({}, {"_id":0, "actor_id":0 , "movies":0}).sort([("name", -1)])
            for i in range(actorMovies.count()):
                print(actorMovies[i])
    elif choice == 3:
        os.system('clear')
        actorName      = raw_input("Please enter name of any actor : ")
        actorMovies = db.actors.aggregate([{"$match": {'name': actorName}} , {"$project" : {"movie_count": {"$size": "$movies"}}}])
        actorMovies = actorMovies.next()
        print("{} has starred in {} movies in total.".format(actorName, actorMovies['movie_count']))
    else:
        os.system('clear')
        actorName      = raw_input("Please enter name of any actor : ")
        actorMovies = db.actors.find({"name":actorName}, {"_id":0, "name":0})
        actorMovies = actorMovies[0]['movies']
        for i in range(len(actorMovies)):
            print(actorMovies[i]['title'])
