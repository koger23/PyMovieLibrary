#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtGui import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QListWidget, QLineEdit

import sys

# Import moduls
from modules import folderBrowser, movieList, movieDetails
from utils import fileUtils

reload(fileUtils)
reload(folderBrowser)
reload(movieList)
reload(movieDetails)

class MovieLibrary(QMainWindow):

    def __init__(self):
        super(MovieLibrary, self).__init__()
        self.setWindowTitle("Movie Library v0.1")
        self.resize(1200, 800)

        centralWidget = QWidget()
        mainLayout = QHBoxLayout(centralWidget)
        self.setCentralWidget(centralWidget)

        # Folder browser
        self.folderBrowser = folderBrowser.FolderBrowser()
        mainLayout.addWidget(self.folderBrowser)

        # Movie list module
        self.movieList = movieList.MovieList(self.folderBrowser.browser)
        mainLayout.addWidget(self.movieList)


        # MOVIE DETAILS MODULE
        self.movieDetail = movieDetails.MovieDetails(self)
        mainLayout.addWidget(self.movieDetail)
        self.movieDetail.setVisible(False)


        self.applyStyle()

    def applyStyle(self):

        with open(fileUtils.getIcon("style"), "r") as styleFile:
            style = styleFile.read()

        self.setStyleSheet(style)


app = QApplication(sys.argv)
window = MovieLibrary()
window.show()
app.exec_()