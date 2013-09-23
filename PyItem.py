#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 17.08.2013

@author: Duncan MC Leod
'''

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QApplication, QFrame, QPalette, QScrollArea, QCursor, QColor
from PyQt4.QtCore import pyqtSignal, QObject, QPoint
from numpy.ma.core import abs



class PyScrollWidget(QScrollArea):
    def __init__(self, _parent=None):
        QScrollArea.__init__(self, _parent)
    
        #self.setMouseTracking(True)
        # ScrollBarAlwaysOff == 1
        # TODO: Finden wo "ScrollBarAlwaysOff" definiert ist und dann einsetzen statt der Zahl
        self.setHorizontalScrollBarPolicy(1)
        
        if _parent:
            self.setGeometry(_parent.geometry())
        else:
            self.setGeometry(1,1,1,1)

        self.btnWidget = QWidget()
        self.oldSizeX = 0
        self.oldSizeY = 0
        self.oldSizeWidth  = 1
        self.oldSizeHeight = 1 
        self.btnWidget.setGeometry(self.oldSizeX, self.oldSizeY, self.oldSizeWidth, self.oldSizeHeight)
        self.setWidget(self.btnWidget)
        
        self.scrollX = 0
        self.scrollY = 0
        
        self.setFrameStyle(1)
        
        # SIGNALS
        self.SIGNAL_onWidthChange = 'SIGNAL_widthchange(PyQt_PyObject)'
        self.SIGNAL_mousepress    = 'SIGNAL_mousepress(PyQt_PyObject)'
        self.SIGNAL_mousemove     = 'SIGNAL_mousemove(PyQt_PyObject)'
        self.SIGNAL_mouserelease  = 'SIGNAL_mouserelease(PyQt_PyObject)'
        

    def resizeEvent(self, _resizeEvent):
        newWidthScrollArea = self.size().width()
        #print("oldWidth:", self.oldSizeWidth, " | newWidth:", newWidth)  
        if newWidthScrollArea != self.oldSizeWidth:
            print(_resizeEvent)
            
            if self.verticalScrollBar().isVisible():
                newWidthBtnWidget = self.width()-self.verticalScrollBar().width()
            else:
                newWidthBtnWidget = self.width()
            
            self.btnWidget.resize(newWidthBtnWidget, self.btnWidget.height())
            self.oldSizeWidth = self.btnWidget.size().width()
            
            print("SIGNAL: ",self.SIGNAL_onWidthChange)
            self.emit(QtCore.SIGNAL(self.SIGNAL_onWidthChange), newWidthBtnWidget-3)
        pass
        
        return QScrollArea.resizeEvent(self, _resizeEvent)


    def onScroll(self):
        self.emit(QtCore.SIGNAL(self.SIGNAL_onScroll))


    def isButtonVisible(self, _button):
        if ( _button.y() > self.scrollY) and (_button.y() < (self.scrollY + self.height()) ):
            return True
        else:
            return False


    def mouseMoveEvent(self, _qmouseevent):
        print("rapante")
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousemove), _qmouseevent)
        return QWidget.mouseMoveEvent(self, _qmouseevent)


    def mousePressEvent(self, _event):
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousepress), _event)
        return QWidget.mousePressEvent(self, _event)


    def mouseReleaseEvent(self, _event):
        self.emit(QtCore.SIGNAL(self.SIGNAL_mouserelease), _event)
        return QWidget.mouseReleaseEvent(self, _event)

#------------------------------------------------------------------------------------------------------------------------------------------#

class PyAbstractItemHandler(QObject):

    def __init__(self, _scrollWidget):
        QObject.__init__(self)
        
        # scrollwidget erhalten und verbinden
        self.scrollWidget = _scrollWidget
        self.btnWidget = self.scrollWidget.btnWidget
        
        ### CONNECTIONS ###
        # WidthChange        
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_onWidthChange), self.slotOnWidthChange)
        # MouseMove
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_mousemove), self.mouseMoveEvent)
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_mousepress), self.mousePressEvent)
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_mouserelease), self.mouseReleaseEvent)
        
        self.buttonHeight = 20
        self.buttonGap = 25
        self.buttonList = []
        self.buttonListVisible = []
        self.buttonListHovered = []
        self.buttonListSelected = []
        self.isMultiSelection = False
        self.buttonListIsEmpty = True
        self.isMousePressed = False
        self.oldMousePos = QPoint(0,0)
        self.mouseMoveDirection = None
        self.mouseVERTICAL = 1
        self.mouseHORIZONTAL = 2
        self.vertScrollbarPosOld = 0
        self.isMouseScroll = False
        print("laenge Buttonlist:",len(self.buttonList))

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def addButton(self, _no, _title):
        x = 0
        if self.buttonListIsEmpty:
            y = (len(self.buttonList))*self.buttonHeight
            self.buttonListIsEmpty = False
        else:
            y = (len(self.buttonList))*(self.buttonHeight+self.buttonGap)

        item = PyItem(self.scrollWidget.btnWidget, self, _no, _title, x, y, self.scrollWidget.width()-20, self.buttonHeight)
        self.btnWidget.resize(self.btnWidget.width(), y+self.buttonHeight)
        self.scrollWidget.resize(self.btnWidget.width(), y+self.buttonHeight)
        item.oY = y 

        self.buttonList.append(item)
        item.setFrameStyle(1)
        if self.isButtonVisible(item):
            item.show()

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def onMouseMove(self, senderEvent):
        print("PyAbstractItemHandler::onMouseMove()")
        (sender, _qmouseevent) = senderEvent
        if sender.isMousePress:
            # scrollen
            pass

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def onMouseHover(self, senderEvent):
        print("PyAbstractItemHandler::onMouseHover()")
        (sender, _qmouseevent) = senderEvent
        for button in self.buttonListHovered:
            button.isHovered = False
            button.decorate()
        del(self.buttonListHovered)
        self.buttonListHovered = []
        sender.isHovered = True
        sender.decorate()
        self.buttonListHovered.append(sender)
        mousePos = self.scrollWidget.mapFromGlobal(QCursor.pos())
        print(mousePos)

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def onMousePressEvent(self, senderEvent):
        (sender, _qmouseevent) = senderEvent
        print("PyAbstractItemHandler::onMousePressEvent()")
        sender.isMousePress = True
        self.isMousePressed = True
        sender.isSelected = True
        sender.decorate()

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def onMouseReleaseEvent(self, senderEvent):
        (sender, _qmouseevent) = senderEvent
        print("PyAbstractItemHandler::onMouseReleaseEvent()")
        # dekorieren & aufräumen
        # wenn beim loslassen der Cursor über dem Button liegt und nicht gescrollt wurde, dann ist er Selected
        sender.isMousePress = False
        if self.isMouseScroll:
            sender.isSelected = False
        else:
            if not self.isMultiSelection:
                for btn in self.buttonListSelected:
                    btn.isSelected = False
                self.buttonListSelected = []
            self.buttonListSelected.append(sender)
        sender.decorate()
        
        self.isMousePressed = False
        self.mouseMoveDirection = None
        self.isMouseScroll = False

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def onScroll(self):
        for button in self.buttonListVisible:
            button.hide()
        
        for button in self.buttonList:
            if self.isButtonVisible(button):
                self.buttonListVisible.append(button)

    #--------------------------------------------------------------------------------------------------------------------------------------#

    def isButtonVisible(self, _button):
        if ( _button.y() > self.scrollWidget.scrollY) and (_button.y() < (self.scrollWidget.scrollY + self.scrollWidget.height()) ):
            return True
        else:
            return False
        
    #--------------------------------------------------------------------------------------------------------------------------------------#

    def mouseMoveEvent(self, _qmouseevent):
        print("PyAbstractItemHandler::mouseMoveEvent()")
        mousePos = self.scrollWidget.mapFromGlobal(QCursor.pos())
        print("oldMousePos:", self.oldMousePos, " | newMousePos:",mousePos)
        if self.isMousePressed:
            vertDelta = mousePos.y()-self.oldMousePos.y()
            horzDelta = mousePos.x()-self.oldMousePos.x()
            print("vertDelta: ", vertDelta)
            print("horzDelta: ", horzDelta)
            if ((abs(vertDelta) > 10) 
                and ((self.mouseMoveDirection == None) or (self.mouseMoveDirection == self.mouseVERTICAL))):
                
                self.mouseMoveDirection = self.mouseVERTICAL
                unterschied = mousePos.y() - self.oldMousePos.y()
                
                scrollbarPosNew = self.vertScrollbarPosOld-unterschied
                print("scrollbarPosOld:", self.vertScrollbarPosOld)
                print("scrollbarPosNew:", scrollbarPosNew)
                self.scrollWidget.verticalScrollBar().setValue(scrollbarPosNew)
                self.isMouseScroll = True
            elif (abs(horzDelta) > 10) and ( (self.mouseMoveDirection == None) or (self.mouseMoveDirection == self.mouseHORIZONTAL) ):
                self.mouseMoveDirection = self.mouseHORIZONTAL
                # 'Zoom' in den Button
        else:
            pass
            for btn in self.buttonListHovered:
                btn.isHovered = False
                btn.decorate()
            self.buttonListHovered = []
        
    #--------------------------------------------------------------------------------------------------------------------------------------#
        
    def mousePressEvent(self, _event):
        print("PyAbstractItemHandler::mousePressEvent()")
        senderEvent = (self, _event)
        mousePos = self.scrollWidget.mapFromGlobal(QCursor.pos())
        self.oldMousePos = mousePos
        self.vertScrollbarPosOld = self.scrollWidget.verticalScrollBar().value()
        self.isMousePressed = True


    def mouseReleaseEvent(self, _event):
        print("PyAbstractItemHandler::mouseReleaseEvent()")
        senderEvent = (self, _event)
        mousePos = self.scrollWidget.mapFromGlobal(QCursor.pos())
        self.oldMousePos = mousePos
        self.isMousePressed = False
        self.isMouseScroll = False


    def slotOnWidthChange(self, _width):
        for btn in self.buttonList:
            btn.resize(_width, btn.size().height())



class PyAbstractItem(QFrame):
    
    def __init__(self, _parent, _itemHandler, _x=0, _y=0, _width=100, _height=20):
        QFrame.__init__(self, _parent)
        print("PyAbstractItem::__init__()")
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
        #print("PyAbstractItem::event()")
        return QWidget.event(self, _qevent)


    def mouseMoveEvent(self, _qmouseevent):
        print("PyAbstractItem::mouseMoveEvent()")
        print(str(_qmouseevent.pos()))
        senderEvent = (self, _qmouseevent)
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousemove), senderEvent)
        return QWidget.mouseMoveEvent(self, _qmouseevent)


    def mousePressEvent(self, _event):
        print("PyAbstractItem::mousePressEvent()")
        senderEvent = (self, _event)
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousepress), senderEvent)
        return QWidget.mousePressEvent(self, _event)


    def mouseReleaseEvent(self, _event):
        print("PyAbstractItem::mouseReleaseEvent()")
        senderEvent = (self, _event)
        self.emit(QtCore.SIGNAL(self.SIGNAL_mouserelease), senderEvent)
        return QWidget.mouseReleaseEvent(self, _event)


    def defineSignals(self, _parent):
        print("PyAbstractItem::defineSignals()")
        self.SIGNAL_mousemove = 'mousemove(PyQt_PyObject)'
        self.SIGNAL_mousepress = 'mousepress(PyQt_PyObject)'
        self.SIGNAL_mouserelease = 'mouserelease(PyQt_PyObject)'
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousemove), self.mousemoveSlot)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousemove), self.itemHandler.onMouseMove)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousemove), self.itemHandler.onMouseHover)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mousepress), self.itemHandler.onMousePressEvent)
        QObject.connect(self, QtCore.SIGNAL(self.SIGNAL_mouserelease), self.itemHandler.onMouseReleaseEvent)
        


    def mousemoveSlot(self, sender):
        print("PyAbstractItem::mousemoveSlot()")
        print("sender:",sender)


    def decorateNormal(self):
        #print("PyAbstractItem::decorateNormal()")
        # Die normalen Anzeigeeinstellungen einstellen
        self.setStyleSheet("background-color: white;");


    def decorateHover(self):
        #print("PyAbstractItem::decorateHover()")
        # Anzeigeeinstellungen wenn Maus rüberfährt
        self.setStyleSheet("background-color: blue;");


    def decorate(self):
        print("PyAbstractItem::decorate()")
        if self.isMousePress:
            if self.isSelected:
                # (halb)Selected, Hovered und selected
                self.decorateHalfselectedAndHoveredAndSelected()
                pass
            else:
                # (halb)Selected und Hovered
                self.decorateHalfselectedAndHovered()
                pass
        elif self.isSelected:
            if self.isHovered:
                # selected und hovered
                self.decorateSelectedAndHovered()
                pass
            else:
                # nur seclected
                self.decorateSelected()
        elif self.isHovered:
            # nur hover
            self.decorateHover()
        else:
            self.decorateNormal()


    def decorateHalfselectedAndHoveredAndSelected(self):
        print("PyAbstractItem::decorateHalfselectedAndHoveredAndSelected()")
        self.setStyleSheet("background-color: green;")


    def decorateHalfselectedAndHovered(self):
        print("PyAbstractItem::decorateHalfselectedAndHovered()")
        self.setStyleSheet("background-color: yellow;")

    def decorateSelectedAndHovered(self):
        print("PyAbstractItem::decorateSelectedAndHovered()")
        self.setStyleSheet("background-color: red;")


    def decorateSelected(self):
        print("PyAbstractItem::decorateSelected()")
        # Anzeigeeinstellungen wenn Objekt z.b. per Mausklick oder Tastaturcursor ausgewählt wurde
        self.setStyleSheet("background-color: orange;")
        pass
    
    def decorateMousepress(self):
        print("PyAbstractItem::decorateMousepress()")
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
