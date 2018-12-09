#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tmdbsimple as tmdb
import os, urllib2, pymongo

tmdb.API_KEY = "ae19b8450bb5b60ea4dad3529cb44d65"


def getMovieDataByTitle(title):
    search = tmdb.Search()
    response = search.movie(query=title)

    posterPathString = "https://image.tmdb.org/t/p/w300/"
    backdropPathString = "https://image.tmdb.org/t/p/w500/"

    returnDic = search.results[0]
    returnDic["poster_path"] = posterPathString + returnDic["poster_path"]

    return returnDic



def downloadPoster(filePath, posterLink):

    posterPath = filePath.replace(".mkv", ".jpg")

    if not os.path.exists(posterPath):
        f = open(posterPath, "wb")
        f.write(urllib2.urlopen(posterLink).read())
        f.close()
    return posterPath