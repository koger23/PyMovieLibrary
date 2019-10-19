#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bson import ObjectId
from pymongo import MongoClient


def get_db_connection():
    client = MongoClient("localhost", 27017)
    db = client["MovieLibrary"]
    collection = db["Movies"]
    return collection


def insert_movie(movie_data):
    return get_db_connection().insert(movie_data)


def get_movies_by_path(file_path):
    collection = get_db_connection()
    result = collection.find_one({"path": file_path})

    return result


def get_movies_by_folder(folder):
    collection = get_db_connection()
    result = collection.find({"folder": folder})

    movies = []

    if result:
        for i in result:
            movies.append(i)
    return movies


def get_movies(movie_id=None, folder=None):
    collection = get_db_connection()

    result = []

    if not movie_id:
        for movie in collection.find({}):
            result.append(movie)

    else:
        result.append(collection.find_one({"_id": ObjectId(movie_id)}))

    if folder:
        result.append(collection.find_one({"poster": ObjectId(movie_id)}))

    return result


def update_movie_status(movie_id, watched_status):
    collection = get_db_connection()

    if watched_status is True:
        collection.update_one({"_id": ObjectId(movie_id)},
                              {"$set": {"watched": watched_status}},
                              upsert=False
                              )
    elif watched_status is False:
        collection.update_one({"_id": ObjectId(movie_id)},
                              {"$set": {"watched": watched_status}},
                              upsert=False
                              )


def delete_movie(movie_id):
    if movie_id:
        collection = get_db_connection()
        collection.delete_one({"_id": ObjectId(movie_id)})


if __name__ == '__main__':
    print get_movies_by_path("D:\\Movies\\Armaged_don.mkv")
