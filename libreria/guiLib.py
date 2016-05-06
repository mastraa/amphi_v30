"""
guiLib.py

Library for gui functions

25/03/2016
Andrea Mastrangelo
"""

from PyQt4 import QtGui
import pyqtgraph as pg

def ImageToLabel(label, url):
	pixMap = QtGui.QPixmap(url)
	label.setPixmap(pixMap)
	label.show()

def plotter(widList,data):
	"""
	for every PlotWidget in widList will plot many graph as number of y in correspondant data list
	widList: PlotWidget list
	data: set of [x,[y]] data, data lenght must be the same of widList lenght
		y could be more than one for each x data
	almost five plot per widget in different color
	"""
	color=[(255,0,0),(0,255,0),(0,0,255),(255,255,255),(200,150,150)]
	try:
		for i in range(len(widList)):
			widList[i].clear()
			for j in range(len(data[i][1])):
				if isinstance(data[i][1][j], list):
					widList[i].plot(data[i][0],data[i][1][j],pen=color[j])
				else:
					widList[i].plot(data[i][0],data[i][1],pen=color[0])
					break
	except (TypeError,Exception): #TypeError->maybe lista won't be a list
		try:
			widList.clear()
			widList.plot(data[0],data[1],pen=(255,0,0))
		except Exception:#caused by an errating usage of pyqtgraph library
			pass
