#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget, QListWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QListWidgetItem, \
    QStyledItemDelegate, QBrush, QColor, QPen, QFont, QPixmap, QStyle     # QItemDelegate akkor kell, ha nem használunk css fájlt cusomizációra

# QBrush - itemek háttérsz0ne
# QPen - körvonalak és szövegek szine
# QColor - csak ezzel lehet a fenti két osztálynak szineket

from PySide.QtCore import QSize, QRect, Qt # QRectF az floating point osztály nem egész méretekhez
import os
from utils import fileUtils

reload(fileUtils)

class MovieList(QWidget):

    def __init__(self, folderBrowser):
        super(MovieList, self).__init__()

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        self.filterField = QLineEdit()
        self.filterField.setObjectName("filterField")
        self.movieList = MovieBrowser(folderBrowser)

        mainLayout.addWidget(self.filterField)
        mainLayout.addWidget(self.movieList)



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

    def setCurrentMovie(self):
        self.currentMovie = self.currentItem().movieObj


    def refresh(self):
        self.clear() # Itt csak egy self kell, mert már benne vagyunk a ListWidget-ben

        for movieObj in self.folderBrowser.movieFiles:
            movieItem = MovieItem(movieObj, self) # a self azért kell, mert ebbe a listába akarjuk ezeket létrehozni


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
        # self.selectedOutline.setWidth(4) # a vonal kirajzolás bugos

        self.font = QFont()
        self.font.setPointSize(13)

    def paint(self, painter, option, index):
        """ Overrideoljuk a saját igényeinkre"""

        rect = option.rect # egérrel kattintásnál megjelenő négyzet bal felső sarkának a helyzete és a szöveg magassága és hossza

        movieObj = index.data(Qt.UserRole)

        # print rect.width(), rect.height() # printeli a méreteket, mert mindig lefut ablakműveletnél

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