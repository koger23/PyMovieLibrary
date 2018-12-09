#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtGui import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPixmap


class MovieDetails(QWidget):

    def __init__(self, mainWindow):
        super(MovieDetails, self).__init__()


        self.mainWindow = mainWindow  # hogy el tudjon minden hideolni
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        self.posterWidget = QLabel()
        self.movieText = QLabel()
        self.movieText.setWordWrap(True)

        self.mainWindow.movieList.movieList.itemDoubleClicked.connect(self.setMovie)

        mainLayout.addWidget(self.posterWidget)
        mainLayout.addWidget(self.movieText)

    def setMovie(self, movieObj):

        self.setVisible(True)

        self.mainWindow.movieList.setVisible(False)
        self.mainWindow.folderBrowser.setVisible(False)

        movieObj = self.mainWindow.movieList.movieList.currentMovie

        self.posterWidget.setPixmap(QPixmap(movieObj.poster))

        self.movieText.setText(movieObj.data["overview"])

