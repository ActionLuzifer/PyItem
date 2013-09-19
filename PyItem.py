#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 17.08.2013

@author: Duncan MC Leod
'''

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QApplication, QLabel, QFrame, QPalette, QScrollArea
from PyQt4.QtCore import QEvent, pyqtSignal, QObject
import PyQt4


class PyAbstractItemHandler(QScrollArea):
    def __init__(self, _parent):
        QScrollArea.__init__(self, _parent)
        self.move(0,0)
        self.buttonHeight = 20
        self.buttonGap = 5
        self.scrollX = 0
        self.scrollY = 0
        self.buttonList = []
        self.buttonListVisible = []
        self.buttonListHovered = []
        self.buttonListIsEmpty = True
        print("laenge Buttonlist:",len(self.buttonList))
        
        self.setFrameStyle(1)
        
        # sich selbst anpassen und anzeigen
        self.resize(_parent.width(), _parent.height())
        self.show()


    def addButton(self, _no, _title):
        x = 0
        if self.buttonListIsEmpty:
            y = (len(self.buttonList))*self.buttonHeight
            self.buttonListIsEmpty = False
        else:
            y = (len(self.buttonList))*(self.buttonHeight+self.buttonGap)

        item = PyItem(self, self, _no, _title, x, y, self.width()-20, self.buttonHeight)
        item.oY = y 

        self.buttonList.append(item)
        item.setFrameStyle(1)
        if self.isButtonVisible(item):
            item.show()


    def resizeEvent(self, _resizeEvent):
        #self.scrollbarVert.move(self.width()-self.scrollbarVert.width(), 0)
        #self.scrollbarVert.resize(self.scrollbarVert.width(), self.height())
        self.scrollArea.setGeometry(self.geometry())
        QWidget.resizeEvent(self, _resizeEvent)


    def onMouseMove(self, senderEvent):
        (sender, _qmouseevent) = senderEvent
        if sender.isMousePress:
            # scrollen
            pass


    def onMouseHover(self, senderEvent):
        (sender, _qmouseevent) = senderEvent
        for button in self.buttonListHovered:
            button.decorateNormal()
        del(self.buttonListHovered)
        self.buttonListHovered = []
        sender.decorateHover()
        self.buttonListHovered.append(sender)
        print("Olé")


    def onMousePressEvent(self, senderEvent):
        (sender, _qmouseevent) = senderEvent
        print("def onMousePressEvent(self, sender):")
        sender.isMousePress = True
        sender.decorate()


    def onMouseReleaseEvent(self, senderEvent):
        (sender, _qmouseevent) = senderEvent
        print("def onMouseReleaseEvent(self, sender):")
        sender.isMousePress = False
        sender.decorate()
        # wenn beim loslassen der Cursor über dem Button liegt, dann ist er Selected


    def onScroll(self):
        for button in self.buttonListVisible:
            button.hide()
        
        for button in self.buttonList:
            if self.isButtonVisible(button):
                self.buttonListVisible.append(button)


    def isButtonVisible(self, _button):
        if ( _button.y() > self.scrollY) and (_button.y() < (self.scrollY + self.height()) ):
            return True
        else:
            return False
        
    def mouseMoveEvent(self, _qmouseevent):
        #self.mouseKoordX = _qmouseevent.
        print(_qmouseevent)
        return QWidget.mouseMoveEvent()
        
        
    def mousePressEvent(self, _event):
        senderEvent = (self, _event)
        return QWidget.mousePressEvent(self, _event)


    def mouseReleaseEvent(self, _event):
        senderEvent = (self, _event)
        return QWidget.mouseReleaseEvent(self, _event)



class PyAbstractItem(QFrame):
    
    def __init__(self, _parent, _itemHandler, _x=0, _y=0, _width=100, _height=20):
        QFrame.__init__(self, _parent)
        self.itemHandler = _itemHandler
        self.isMousePress = False
        self.isSelected = False
        self.isHovered = False
        self.decorateNormal()
        self.defineSignals(_parent)
        self.move(_x,_y)
        self.resize(_width,_height)
        self.show()


    def event(self, _qevent):
        return QWidget.event(self, _qevent)


    def mouseMoveEvent(self, _qmouseevent):
        print(str(_qmouseevent.pos()))
        senderEvent = (self, _qmouseevent)
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousemove), senderEvent)
        return QWidget.mouseMoveEvent(self, _qmouseevent)


    def mousePressEvent(self, _event):
        senderEvent = (self, _event)
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousepress), senderEvent)
        return QWidget.mousePressEvent(self, _event)


    def mouseReleaseEvent(self, _event):
        senderEvent = (self, _event)
        self.emit(QtCore.SIGNAL(self.SIGNAL_mouserelease), senderEvent)
        return QWidget.mouseReleaseEvent(self, _event)


    def defineSignals(self, _parent):
        self.SIGNAL_mousemove = 'mousemove(PyQt_PyObject)'
        self.SIGNAL_mousepress = 'mousepress(PyQt_PyObject)'
        self.SIGNAL_mouserelease = 'mouserelease(PyQt_PyObject)'
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousemove), self.mousemoveSlot)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousemove), self.itemHandler.onMouseMove)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousemove), self.itemHandler.onMouseHover)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousepress), self.itemHandler.onMousePressEvent)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mouserelease), self.itemHandler.onMouseReleaseEvent)
        


    def mousemoveSlot(self, sender):
        print("sender:",sender)


    def decorateNormal(self):
        # Die normalen Anzeigeeinstellungen einstellen
        self.setStyleSheet("background-color: white;");


    def decorateHover(self):
        # Anzeigeeinstellungen wenn Maus rüberfährt
        self.setStyleSheet("background-color: blue;");


    def decorate(self):
        if self.isMousePress:
            if self.isSelected:
                # (halb)Selected, Hovered und selected
                pass
            else:
                # (halb)Selected und Hovered
                pass
        elif self.isSelected:
            if self.isHovered:
                # selected und hovered
                pass
            else:
                # nur seclected
                self.decorateSelected()
        elif self.isHovered:
            # nur hover
            self.decorateHover()
        else:
            self.decorateNormal()


    def decorateSelected(self):
        # Anzeigeeinstellungen wenn Objekt z.b. per Mausklick oder Tastaturcursor ausgewählt wurde
        pass
    
    def decorateMousepress(self):
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        

class PyItem(PyAbstractItem):
    
    def __init__(self, _parent, _itemHandler, _number, _title, _x, _y, _width, _height):
        PyAbstractItem.__init__(self, _parent, _itemHandler, _x, _y, _width, _height)
        PyAbstractItem.setMouseTracking(self, True)
        self.number = _number
        self.title = _title
        self.titleLabel = QtGui.QLabel(self)
        self.titleLabel.setText(self.title)
        self.titleLabel.show()
        


if __name__ == '__main__':
    qapp = QApplication(sys.argv);
    #newgui = PyItem()
    sys.exit(qapp.exec_()) 
