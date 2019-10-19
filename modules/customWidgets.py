#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtGui import QWidget, QPainter, QBrush, QPen, QColor, QPixmap
from PySide.QtCore import Signal, Qt
import os


ICONS = os.path.dirname(__file__).replace("modules", "images")

class IconButton(QWidget):

    """
    Custom icon button for back click
    """

    clicked = Signal()

    def __init__(self, icon, tooltip):
        super(IconButton, self).__init__()

        self.icon = os.path.join(ICONS, icon)
        self.setToolTip(tooltip)
        self.setFixedSize(32, 32)
        self.outLinePen = QPen(QColor("white"))
        self.isHighlighted = False


    def paintEvent(self, event):

        painter = QPainter()

        painter.begin(self) # át kell adni a widgetet amiben a painter rajzol

        self.drawWidget(painter)



        painter.end()

    def drawWidget(self, painter):

        if self.isHighlighted:
            painter.setOpacity(1.0)
        else:
            painter.setOpacity(0.5)

        pixmap = QPixmap(self.icon)
        pixmap = pixmap.scaledToWidth(self.width(), Qt.SmoothTransformation)  # Resizeolni kell, hogy ne legyne pixeles
        painter.drawPixmap(self.rect(), pixmap)

    def enterEvent(self, event):
        self.isHighlighted = True
        self.repaint()

    def leaveEvent(self, event):
        self.isHighlighted = False
        self.repaint()

    def mousePressEvent(self, event):
        self.clicked.emit()

class MyProgress(QWidget):

    def __init__(self):
        super(MyProgress, self).__init__()

        self.setMaximumHeight(50)

        self.maxValue = 100
        self.currentValue = 0

        self.outLine = QPen(QColor("#999999"))
        self.fillColor = QBrush(QColor("green"))
        self.textPen = QPen(QColor("black"))

    def setMaximum(self, value):
        self.maxValue = value

    def stepProgress(self):
        self.currentValue += 1
        self.repaint()

    def paintEvent(self, event):

        painter = QPainter()

        painter.begin(self) # át kell adni a widgetet amiben a painter rajzol

        self.drawWidget(painter)

    def drawWidget(self, painter):

        rect = self.rect()

        # draw progress
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.fillColor)
        painter.drawRect(rect.x(), rect.y(), self.currentValue, rect.height()-1)

        # draw an outline
        painter.setPen(self.outLine)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect.x(), rect.y(), rect.width()-1, rect.height()-1)


        # draw text on progress

        painter.setPen(self.textPen)
        painter.drawText(rect, "My Progress 0%")



if __name__ == '__main__':

    from PySide.QtGui import QApplication, QVBoxLayout
    import sys, time

    class TestWindow(QWidget):

        def __init__(self):
            super(TestWindow, self).__init__()

            self.resize(500, 500)

            self.setLayout(QVBoxLayout())

            self.iconButton = IconButton(os.path.join(ICONS, "icon_back.png"), "Testing IconButton")
            self.layout().addWidget(self.iconButton)


            # testing progressbar

            self.myProgress = MyProgress()

            self.layout().addWidget (self.myProgress)



            self.setStyleSheet("QWidget {background-color:black}")

    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()

    for i in range(window.myProgress.width()):
        window.myProgress.stepProgress()
        QApplication.processEvents()
        time.sleep(0.05)

    app.exec_()

