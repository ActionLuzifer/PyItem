#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created on 29.08.2013

@author: Duncan MC Leod
'''

import sys

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QApplication

import PyItem


class myWidget(QWidget):

    def __init__(self, _parent=None):
        QWidget.__init__(self, _parent)
        # create buttonHandler
        self.btnHandler = PyItem.PyAbstractItemHandler(self)
        self.btnHandler.show()

    
    def resizeEvent(self, _resizeEvent):
        self.btnHandler.resize(self.size())

if __name__ == '__main__':
    # create application
    qapp = QApplication(sys.argv)
    
    
    # create mainwindow
    mainwidget = myWidget()
    mainwidget.show()
    

    # add Buttons
    mainwidget.btnHandler.addButton("#01", "Titel01")
    mainwidget.btnHandler.addButton("#02", "Titel02")
    mainwidget.btnHandler.addButton("#03", "Titel03")
    mainwidget.btnHandler.addButton("#04", "Titel04")
    mainwidget.btnHandler.addButton("#05", "Titel05")
    mainwidget.btnHandler.addButton("#06", "Titel06")
    mainwidget.btnHandler.addButton("#07", "Titel07")
    mainwidget.btnHandler.addButton("#08", "Titel08")
    mainwidget.btnHandler.addButton("#09", "Titel09")
    mainwidget.btnHandler.addButton("#10", "Titel10")
    mainwidget.btnHandler.addButton("#11", "Titel11")
    mainwidget.btnHandler.addButton("#12", "Titel12")
    mainwidget.btnHandler.addButton("#13", "Titel13")
    mainwidget.btnHandler.addButton("#14", "Titel14")
    mainwidget.btnHandler.addButton("#15", "Titel15")
    mainwidget.btnHandler.addButton("#16", "Titel16")
    
    # start application
    sys.exit(qapp.exec_()) 
