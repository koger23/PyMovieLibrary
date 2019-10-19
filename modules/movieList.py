#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget, QListWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QListWidgetItem, \
    QStyledItemDelegate, QBrush, QColor, QPen, QFont, QPixmap, QStyle, QMessageBox     # QItemDelegate akkor kell, ha nem használunk css fájlt cusomizációra

# QBrush - itemek háttérsz0ne
# QPen - körvonalak és szövegek szine
# QColor - csak ezzel lehet a fenti két osztálynak szineket

from PySide.QtCore import QSize, QRect, Qt # QRectF az floating point osztály nem egész méretekhez
from utils import fileUtils, DB_utils
from modules import customWidgets

reload(fileUtils)
reload(customWidgets)

class MovieList(QWidget):

    def __init__(self, folderBrowser):
        super(MovieList, self).__init__()

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        filterLayout = QHBoxLayout()
        mainLayout.addLayout(filterLayout)

        self.setWatchedButton = customWidgets.IconButton("icon_watchList.png", "Set as watched")
        filterLayout.addWidget(self.setWatchedButton)

        self.setHideWatchedButton = customWidgets.IconButton("filter_icon.png", "Set as watched")
        filterLayout.addWidget(self.setHideWatchedButton)

        self.filterField = QLineEdit()
        self.filterField.setObjectName("filterField")
        filterLayout.addWidget(self.filterField)

        self.movieList = MovieBrowser(folderBrowser)
        mainLayout.addWidget(self.movieList)


        self.progressBar = customWidgets.MyProgress()
        mainLayout.addWidget(self.progressBar)
        self.progressBar.setVisible(True)

        self.setWatchedButton.clicked.connect(self.movieList.setWatched)
        self.setHideWatchedButton.clicked.connect(self.movieList.hideWatched)


class MovieBrowser(QListWidget):

    def __init__(self, folderBrowser):
        super(MovieBrowser, self).__init__()

        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(10)
        # ItemDelegate egy Painter osztály. Azért dolgozik, hogy hogyan rajzolódjon ki a lista tartalma
        self.setItemDelegate(MyDelegate())

        self.currentMovie = None


        self.folderBrowser = folderBrowser
        self.folderBrowser.itemClicked.connect(self.refresh)

        self.itemDoubleClicked.connect(self.setCurrentMovie)
        self.itemClicked.connect(self.getSelectedMovie)

        # connect downloader signal to repaint self
        self.folderBrowser.dataDownloader.downloadFinished.connect(self.repaint)

    def setCurrentMovie(self):
        self.currentMovie = self.currentItem().movieObj

    def getMoviesQty(self):
        print "Number of movies: " + str(self.count())

    def getSelectedMovie(self):
        currentItem = self.currentItem()
        if currentItem:
            curMovieObj = currentItem.data(Qt.UserRole)
            return curMovieObj

    def keyPressEvent(self, event):

        selectedMovie = self.getSelectedMovie()

        # If delete button is pressed:
        if event.key() == Qt.Key_Delete:
            if not selectedMovie: return

            poster = selectedMovie.path[:-4] + ".jpg"

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Are you sure you want to delete %s? \nThe file will be deleted as well." % selectedMovie.name)
            msg.setWindowTitle("Deleting movie")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            if msg.exec_() == QMessageBox.Ok:
                print "Deleting: " + str(selectedMovie.name)

                try:
                    DB_utils.deleteMovie(selectedMovie.id)
                    print "Movie deleted from MongoDB..."
                except:
                    print "Error deleting movie from MongoDB " + str(selectedMovie.id)
                try:
                    fileUtils.deleteMovieFile(selectedMovie.path)
                    print "Movie file deleted..."
                except:
                    print "Error deleting movie file: " + str(selectedMovie.path)
                try:
                    fileUtils.deleteMovieFile(poster)
                    print "Deleting poster: " + str(poster)
                except:
                    print "Error deleting movie poster: " + str(poster)

                self.takeItem(self.row(self.currentItem()))
                selectedMovie.delete()

    def setWatched(self):

        selectedMovie =  self.getSelectedMovie()

        if selectedMovie:
            # selectedMovie.setMovieAsWatched()
            if selectedMovie.watched == 0:
                selectedMovie.watched = 1
                DB_utils.updateMovieStatus(selectedMovie.id, selectedMovie.watched)
            else:
                selectedMovie.watched = 0
                DB_utils.updateMovieStatus(selectedMovie.id, selectedMovie.watched)

            self.refresh()

    def hideWatched(self):

        self.Movie

        self.refresh()

    def refresh(self):
        self.clear() # Itt csak egy self kell, mert már benne vagyunk a ListWidget-ben

        for movieObj in self.folderBrowser.movieObjects:
            movieItem = MovieItem(movieObj, self) # a self azért kell, mert ebbe a listába akarjuk ezeket létrehozni
        self.getMoviesQty()

class MovieItem(QListWidgetItem):

    def __init__(self, movieObj, parent):
        super(MovieItem, self).__init__(parent)

        self.movieObj = movieObj

        self.setSizeHint(QSize(310, 500)) # ez valójában a helyfoglalást állitja be

        self.setData(Qt.UserRole, movieObj) # itt adatot hozunk létre, amit át tud adni Q itemeknek. Ez egy channel

class MyDelegate(QStyledItemDelegate):

    def __init__(self):
        super(MyDelegate, self).__init__()

        self.bgColor = QBrush(QColor("#333333"))
        self.outlineColor = QPen(QColor("#555555"))

        self.posterBrush = QBrush(QColor("#000000"))
        self.posterOutline = QPen(QColor("#ffffff"))
        self.selectedColor = QBrush(QColor("#777777"))
        self.selectedOutline = QPen(QColor("#999999"))
        self.transparentBG = QBrush(QColor(255, 255, 255, 60))
        self.watchedBG = QBrush(QColor(0, 0, 0, 180))
        self.unWatchedBG = QBrush(QColor(0, 0, 0, 0))
        # self.selectedOutline.setWidth(4) # a vonal kirajzolás bugos

        self.font = QFont()
        self.font.setPointSize(13)

    def paint(self, painter, option, index):
        """ Overrideoljuk a saját igényeinkre"""

        rect = option.rect # egérrel kattintásnál megjelenő négyzet bal felső sarkának a helyzete és a szöveg magassága és hossza

        movieObj = index.data(Qt.UserRole)

        # BACKGROUND rect

        painter.setPen(Qt.NoPen)

        if option.state & QStyle.State_Selected:
            painter.setBrush(self.selectedColor)
        else:
            painter.setBrush(self.bgColor)


        # átadjuk a négyzet rajzoló függvénynek az itemek bal felső poz0cióit, més megadjuk a méretet
        painter.drawRect(rect)

        # POSTER rect
        painter.setBrush(self.posterBrush)
        painter.setPen(self.posterOutline)

        # Posert image rect
        pixmap = QPixmap(movieObj.poster)
        pixmapRect = QRect(rect.x() + 5, rect.y() + 5, pixmap.width(), pixmap.height())
        painter.drawPixmap(pixmapRect, pixmap)

        # TITLE rect
        painter.setFont(self.font)
        titleRect = QRect(pixmapRect.left(), pixmapRect.bottom(), pixmapRect.width(), 40)
        painter.drawText(titleRect, Qt.AlignVCenter | Qt.AlignHCenter, movieObj.name)


        if option.state & QStyle.State_Selected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.transparentBG)
            painter.drawRect(rect)

        if movieObj.getMovieWatchedStatus() == 1:

            watchedRect = QRect(rect.x() + 2, rect.y() + 2, 25, 25)
            watchedIcon = QPixmap(fileUtils.getIcon("watchedfiltericon"))
            painter.setBrush(self.watchedBG)
            painter.drawPixmap(watchedRect, watchedIcon)
            painter.setBrush(self.watchedBG)
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRect(rect.x()-2, rect.y()-2, rect.width()+4, rect.height()+4))

        elif movieObj.getMovieWatchedStatus() == 0:
            painter.setBrush(self.unWatchedBG)
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRect(rect.x()-2, rect.y()-2, rect.width()+4, rect.height()+4))