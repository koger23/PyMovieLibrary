#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import QObject, Signal
import Queue, threading
from utils import DB_utils
import tmdbsimple as tmdb
import os, urllib2

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

        # download datas in seperate thread if it is done, pass to movie object
        movieData = getMovieDataFromTMDB(movieObj.name)

        posterPath = downloadPoster(movieObj.path, movieData["poster_path"])

        movieData["poster"] = posterPath
        movieData["path"] = movieObj.path
        movieData["watched"] = 0

        # Store datas into MongoDB
        movieData["_id"] = DB_utils.insertMovie(movieData)

        # Setup for movie object
        movieObj.setData(movieData)

        dataDownloader.downloadFinished.emit()


class DataDownloader(QObject):

    downloadFinished = Signal()

    def __init__(self):
        super(DataDownloader, self).__init__()

        self.queue = Queue.Queue() # egy thread save lista, tudnak a threadek pullolni adatot, stb.


    def addMovie(self, movieFile):
        self.queue.put(movieFile) # Queue-hoz hozzáadjuk

    def startDownload(self):
        for i in range(3):
            t = threading.Thread(target=downloadWorker, args=(self.queue, self))
            # a self azért lett átadva,
            # hogy a dowdnload finished Signal-hoz hozzáférjünk
            t.start()


