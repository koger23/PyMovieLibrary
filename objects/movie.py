#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import fileUtils, DB_utils
import os

reload(fileUtils)
reload(DB_utils)


class Movie():

    def __init__(self, path):
        self.id = None
        self.path = path
        self.name = self.setName()
        self.originalTitle = None
        self.description = None
        self.date = None
        self.watched = None
        self.poster = fileUtils.getIcon("collectingData")
        self.backdrop = None

        # self.setData()

    def setName(self):
        return os.path.basename(self.path)[:-4]
        # return self.path.split("\\")[-1].replace(".mkv", "")

    def setData(self, movieData=None):
        """For MongoDB"""

        if movieData:
            self.id = movieData["_id"]
            self.date = movieData["release_date"]
            self.originalTitle = movieData["original_title"]
            self.poster = movieData["poster"]
            self.description = movieData["overview"]
            self.backdrop = movieData["backdrop_path"]
            self.watched = movieData["watched"]

    def startMovie(self):
        os.startfile(self.path)

    def getMovieWatchedStatus(self):
        return self.watched

    def setMovieAsWatched(self):
        if self.watched == 0:
            self.watched = 1
        elif self.watched == 1:
            self.watched = 0

    def delete(self):

        pass

    def copy(self):

        pass