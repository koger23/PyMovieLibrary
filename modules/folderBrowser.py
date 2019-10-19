#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import platform

from PySide.QtGui import QWidget, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidgetItem, \
    QIcon

from objects import movie, dataDownloader
from utils import fileUtils, DB_utils

reload(fileUtils)
reload(movie)
reload(DB_utils)
reload(dataDownloader)


class FolderBrowser(QWidget):

    def __init__(self):
        super(FolderBrowser, self).__init__()
        self.setMaximumWidth(300)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        self.browser = BrowserView()
        mainLayout.addWidget(self.browser)

        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        addFolder_btnn = QPushButton("Add Folder")
        addFolder_btnn.clicked.connect(self.addFolder)

        removeFolder_bttn = QPushButton("Remove Folder")
        removeFolder_bttn.clicked.connect(self.removeFolder)

        buttonLayout.addWidget(addFolder_btnn)
        buttonLayout.addWidget(removeFolder_bttn)

        # Load config file
        self.config = fileUtils.load_config()
        self.browser.refreshView(self.config)

        # Progressbar

    def addFolder(self):

        folder = QFileDialog.getExistingDirectory(self, "Select folder")

        if len(folder):

            if folder not in self.config["folders"]:
                self.config["folders"].append(folder)

            fileUtils.save_config(self.config)
            self.browser.refreshView(self.config)

    def removeFolder(self):

        if not self.browser.currentItem():
            return

        folderPath = self.browser.currentItem().path

        self.config["folders"].remove(folderPath)

        fileUtils.save_config(self.config)

        self.browser.refreshView(self.config)


class BrowserView(QListWidget):

    def __init__(self):
        super(BrowserView, self).__init__()

        self.currentFolder = None

        self.movieObjects = []

        self.itemClicked.connect(self.setCurrentFolder)

        self.dataDownloader = dataDownloader.DataDownloader()

    def setCurrentFolder(self):

        self.movieObjects = []
        self.currentFolder = self.currentItem().path

        files = fileUtils.get_movies(self.currentFolder)

        for filePath in files:
            movieObj = movie.Movie(filePath)

            # Check in DataBase
            movieData = DB_utils.get_movies_by_path(movieObj.path)

            if movieData:
                movieObj.setData(movieData)
            else:
                self.dataDownloader.addMovie(movieObj)

            self.movieObjects.append(movieObj)

        self.dataDownloader.startDownload()

    def refreshView(self, config):
        self.clear()

        for path in config["folders"]:
            item = FolderItem(path, self)

    def dummy(self):
        pass


class FolderItem(QListWidgetItem):

    def __init__(self, path, parent):
        super(FolderItem, self).__init__(parent)

        folderName = ""

        self.path = path

        if platform == "linux" or platform == "linux2":
            folderName = path.split("/")[-1]
        elif platform == "win32":
            folderName = path.split("\\")[-1]

        self.setText(folderName)
        self.setToolTip(path)
        self.setIcon(QIcon(fileUtils.get_icon("folder")))


if __name__ == '__main__':
    from PySide.QtGui import QApplication
    import sys

    app = QApplication(sys.argv)
    win = FolderBrowser()
    win.show()
    app.exec_()
