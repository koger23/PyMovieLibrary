#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import fileUtils, DB_utils
import os

reload(fileUtils)
reload(DB_utils)


class Movie():

    def __init__(self, path):
        self.path = path
        self.name = self.setName()
        self.dataFile = path.replace(".mkv", ".json")
        self.date = None
        self.watched = False
        self.poster = fileUtils.getIcon("collectingData")
        self.data = self.getData()


    def setName(self):
        return os.path.basename(self.path).upper()[:-4]

    def getData(self):

        if not os.path.exists(self.dataFile):
            data = DB_utils.getMovieDataByTitle(self.name)
        else:
            data = fileUtils.loadMovieData(self.dataFile)

        if data:
            # Save datas as JSON file next to the movie
            fileUtils.saveMovieData(self.dataFile, data)

            self.name = data["title"]
            self.date = data["release_date"]

            # Download Poster
            self.poster = DB_utils.downloadPoster(self.path, data["poster_path"])

            return data

        return {}


    def delete(self):

        pass

    def copy(self):

        pass