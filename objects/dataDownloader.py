#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import os
import threading
import urllib2

import tmdbsimple as tmdb
from PySide.QtCore import QObject, Signal

from utils import DB_utils

reload(tmdb)
reload(DB_utils)

tmdb.API_KEY = "ae19b8450bb5b60ea4dad3529cb44d65"


def getMovieDataFromTMDB(title):
    search = tmdb.Search()
    response = search.movie(query=title)
    posterPathString = "https://image.tmdb.org/t/p/w300/"
    backdropPathString = "https://image.tmdb.org/t/p/w500/"

    returnDic = search.results[0]
    returnDic["poster_path"] = posterPathString + returnDic["poster_path"]
    print "Download datas from TMDB"
    return returnDic


def downloadPoster(filePath, posterLink):
    posterPath = filePath.replace(".mkv", ".jpg")

    if not os.path.exists(posterPath):
        print "Downloaded poster " + str(os.path.basename(filePath))
        f = open(posterPath, "wb")
        f.write(urllib2.urlopen(posterLink).read())
        f.close()
    return posterPath


def downloadWorker(queue, dataDownloader):
    while not queue.empty():
        movieObj = queue.get()

        movieData = getMovieDataFromTMDB(movieObj.name)

        posterPath = downloadPoster(movieObj.path, movieData["poster_path"])

        movieData["poster"] = posterPath
        movieData["path"] = movieObj.path
        movieData["watched"] = 0
        movieData["_id"] = DB_utils.insert_movie(movieData)

        movieObj.setData(movieData)

        dataDownloader.downloadFinished.emit()


class DataDownloader(QObject):
    downloadFinished = Signal()

    def __init__(self):
        super(DataDownloader, self).__init__()

        self.queue = Queue.Queue()

    def addMovie(self, movieFile):
        self.queue.put(movieFile)

    def startDownload(self):
        for i in range(3):
            t = threading.Thread(target=downloadWorker, args=(self.queue, self))
            t.start()
