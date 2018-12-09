#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidgetItem, \
    QIcon
from sys import platform
from utils import fileUtils
from objects import movie

reload(fileUtils)
reload(movie)

class FolderBrowser(QWidget):

    def __init__(self):
        super(FolderBrowser, self).__init__()
        self.setMaximumWidth(300)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)  # kell, hogy a modulok egyforman illeszkedjenek
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
        self.config = fileUtils.loadConfig()
        self.browser.refreshView(self.config)

    def addFolder(self):

        folder = QFileDialog.getExistingDirectory(self, "Select folder")

        if len(folder):

            if not folder in self.config["folders"]:
                self.config["folders"].append(folder)

            fileUtils.saveConfig(self.config)
            self.browser.refreshView(self.config)

    def removeFolder(self):

        if not self.browser.currentItem(): return

        folderPath = self.browser.currentItem().path

        self.config["folders"].remove(folderPath)

        fileUtils.saveConfig(self.config)

        self.browser.refreshView(self.config)


class BrowserView(QListWidget):
    """
    Erre azert van szukseg, mert ha pl. torlok egy mappat, akkor nem akarom, hogy a browser resze legyen
    """

    def __init__(self):
        super(BrowserView, self).__init__()

        self.currentFolder = None # feltöltődik későbbi meghíváskor, hogy elkerüljük az attr. errort

        self.movieFiles = []

        self.itemClicked.connect(self.setCurrentFolder)

    def setCurrentFolder(self):

        self.currentFolder = self.currentItem().path

        self.movieFiles = []

        for file in fileUtils.getMovies(self.currentFolder):

            movieObj = movie.Movie(file)

            self.movieFiles.append(movieObj)


        # self.movieFiles = fileUtils.getMovies(self.currentFolder)

    def refreshView(self, config):
        self.clear()

        for path in config["folders"]:
            item = FolderItem(path, self)

    def dummy(self):
        pass


class FolderItem(QListWidgetItem):
    """
    Azert hoztuk letre, hogy tarolni tudjuk az utvonalat kulon es az utolso mappat is.
    """

    def __init__(self, path, parent):
        super(FolderItem, self).__init__(parent)

        self.path = path

        if platform == "linux" or platform == "linux2":
            folderName = path.split("/")[-1]
        elif platform == "win32":
            folderName = path.split("\\")[-1]

        self.setText(folderName)
        self.setToolTip(path)
        self.setIcon(QIcon(fileUtils.getIcon("folder")))


if __name__ == '__main__':
    from PySide.QtGui import QApplication
    import sys

    app = QApplication(sys.argv)
    win = FolderBrowser()
    win.show()
    app.exec_()