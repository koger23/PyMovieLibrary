#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pymongo import MongoClient
from bson import ObjectId

# MongoDB
def getDBconnection():
    client = MongoClient("localhost", 27017)
    db = client["MovieLibrary"]
    collection = db["Movies"]
    return collection

def insertMovie(movieData):
    return getDBconnection().insert(movieData)

def getMoviesByPath(filePath):
    collection = getDBconnection()
    result = collection.find_one({"path": filePath})

    return result


def getMoviesByFolder(folder):
    collection = getDBconnection()
    result = collection.find({"folder": folder})

    movies = []

    if result:
        for i in result:
            movies.append(i)
    return movies


def getMovies(id = None, folder = None):

    collection = getDBconnection()

    result = []

    if not id:
        for movie in collection.find({}):
            result.append(movie)

    else:
        result.append(collection.find_one({"_id":ObjectId(id)}))

    if folder:
        result.append(collection.find_one({"poster":ObjectId(id)}))


    return result

def updateMovieStatus(id, watchedStatus):

    collection = getDBconnection()


    if watchedStatus == True:
        collection.update_one({"_id": ObjectId(id)},
                              {"$set":{"watched": watchedStatus}},
                              upsert=False
                              )
    elif watchedStatus == False:
        collection.update_one({"_id": ObjectId(id)},
                              {"$set":{"watched": watchedStatus}},
                              upsert=False
                              )


def deleteMovie(id):

    if id:
        collection = getDBconnection()
        collection.delete_one({"_id": ObjectId(id)})





if __name__ == '__main__':

    print getMoviesByPath("D:\\Movies\\Armaged_don.mkv")