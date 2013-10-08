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
    scrollWidget.move(400,100)
    scrollWidget.resize(800, 600)
    btnHandler = PyItem.PyAbstractItemHandler(scrollWidget)
    print("ScrollBar.width():",scrollWidget.verticalScrollBar().width())
    scrollWidget.show()
    print("ScrollBar.width():",scrollWidget.verticalScrollBar().width())
    
    
    

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
    btnHandler.addButton("#17", "Titel17")
    btnHandler.addButton("#18", "Titel18")
    btnHandler.addButton("#19", "Titel19")
    btnHandler.addButton("#20", "Titel20")
    btnHandler.addButton("#21", "Titel21")
    #btnHandler.addButton("#22", "Titel22")
    #btnHandler.addButton("#23", "Titel23")
    #btnHandler.addButton("#24", "Titel24")
    #btnHandler.addButton("#25", "Titel25")
    #btnHandler.addButton("#26", "Titel26")
    #btnHandler.addButton("#27", "Titel27")
    #btnHandler.addButton("#28", "Titel28")
    #btnHandler.addButton("#29", "Titel29")
    
    if scrollWidget.verticalScrollBar().maximum() != scrollWidget.verticalScrollBar().minimum():
        scrollWidget.emit(PyItem.QtCore.SIGNAL(scrollWidget.SIGNAL_onWidthChange), scrollWidget.getWidthForButtons())
    
    # start application
    sys.exit(qapp.exec_()) 
