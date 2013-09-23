#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created on 29.08.2013

@author: Duncan MC Leod
'''

import sys

from PyQt4.QtGui import QApplication

import PyItem


if __name__ == '__main__':
    # create application
    qapp = QApplication(sys.argv)
    
    
    # create mainwindow
    scrollWidget = PyItem.PyScrollWidget()
    scrollWidget.move(100,100)
    scrollWidget.resize(800, 600)
    btnHandler = PyItem.PyAbstractItemHandler(scrollWidget)
    scrollWidget.show()

    
    
    

    # add Buttons
    btnHandler.addButton("#01", "Titel01")
    btnHandler.addButton("#02", "Titel02")
    btnHandler.addButton("#03", "Titel03")
    btnHandler.addButton("#04", "Titel04")
    btnHandler.addButton("#05", "Titel05")
    btnHandler.addButton("#06", "Titel06")
    btnHandler.addButton("#07", "Titel07")
    btnHandler.addButton("#08", "Titel08")
    btnHandler.addButton("#09", "Titel09")
    btnHandler.addButton("#10", "Titel10")
    btnHandler.addButton("#11", "Titel11")
    btnHandler.addButton("#12", "Titel12")
    btnHandler.addButton("#13", "Titel13")
    btnHandler.addButton("#14", "Titel14")
    btnHandler.addButton("#15", "Titel15")
    btnHandler.addButton("#16", "Titel16")
    
    # start application
    sys.exit(qapp.exec_()) 
