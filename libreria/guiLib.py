"""
guiLib.py

Library for gui functions

25/03/2016
Andrea Mastrangelo
"""

from PyQt4 import QtGui

def ImageToLabel(label, url):
	pixMap = QtGui.QPixmap(url)
	label.setPixmap(pixMap)
	label.show()