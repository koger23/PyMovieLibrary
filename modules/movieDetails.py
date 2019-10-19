#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtGui import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPixmap
import customWidgets

reload(customWidgets)


class MovieDetails(QWidget):

    def __init__(self, mainWindow):
        super(MovieDetails, self).__init__()

        self.mainWindow = mainWindow  # hogy el tudjon minden hideolni
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        topButtonLayout = QHBoxLayout()
        mainLayout.addLayout(topButtonLayout)
        backButton = customWidgets.IconButton("icon_back.png", "Back to movies")
        topButtonLayout.addWidget(backButton)
        backButton.clicked.connect(self.backClickedAction)

        playButton = customWidgets.IconButton("icon_play.png", "Play movie")
        topButtonLayout.addWidget(playButton)
        playButton.clicked.connect(self.playAction)

        detailsLayout = QHBoxLayout()
        mainLayout.addLayout(detailsLayout)

        self.posterWidget = QLabel()
        self.movieText = QLabel()
        self.movieText.setWordWrap(True)

        self.mainWindow.movieList.movieList.itemDoubleClicked.connect(self.setMovie)

        detailsLayout.addWidget(self.posterWidget)
        detailsLayout.addWidget(self.movieText)

    def setMovie(self):

        self.setVisible(True)

        self.mainWindow.movieList.setVisible(False)
        self.mainWindow.folderBrowser.setVisible(False)

        self.currentMovieObj = self.mainWindow.movieList.movieList.currentMovie

        self.posterWidget.setPixmap(QPixmap(self.currentMovieObj.poster))

        self.movieText.setText(self.currentMovieObj.description)

    def backClickedAction(self):

        self.setVisible(False)

        self.mainWindow.movieList.setVisible(True)
        self.mainWindow.folderBrowser.setVisible(True)

        movieObj = self.mainWindow.movieList.movieList.currentMovie

        self.posterWidget.setPixmap(QPixmap(movieObj.poster))

        self.movieText.setText(movieObj.description)

    def playAction(self):
        self.currentMovieObj.startMovie()