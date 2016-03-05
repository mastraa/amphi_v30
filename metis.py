#!usr/bin/python

# cd programmazione/programmi/python/amphi_v30cd desktop/andrea/programmazione/programmi/python/amphi_v30


import sys, serial
from PyQt4 import QtCore, QtGui, uic
import time
import struct

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np

sys.path.append('libreria')

import comLib, mvpl

#global definition
gui = "gui/MainGui.ui"
baudValues=["9600","57600","115200"]

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		#variables
		global baudList, gui
		self.connStat = 0
		self.device = 0 #device to connect
		self.interval=300 #millis
		self.time=time.strftime("%H:%m:%S")
		self.timer=QtCore.QTimer(self)
		self.timer.timeout.connect(self.timerFunctions)
		self.timer.start(self.interval)

		self.figureSet()
		self.guiSetting()
		self.buttonFunction()

		self.ui.show()

	def guiSetting(self):
		self.ui=uic.loadUi(gui)#load gui
		self.ui.BaudList.addItems(baudValues)
		self.ui.connectionInfo.setReadOnly(1) #it will be scrollable
		self.ui.infusionPlot.addWidget(self.canvasInlet)

	def figureSet(self):
		self.fig_Inlet=Figure()
		self.canvasInlet=FigureCanvas(self.fig_Inlet)

	def buttonFunction(self):#connect button to relative function
		self.ui.DeviceButton.clicked.connect(self.SerialCheck)
		self.ui.addValueButton.clicked.connect(self.addBaud)
		self.ui.ConnectionButton.clicked.connect(self.Connection)

	def SerialCheck(self):#control device connected
		self.ui.DeviceList.clear()
		self.ui.DeviceList.addItems(comLib.checkSerialDevice())

	def addBaud(self):#adding new baud value to the list
		self.ui.BaudList.addItem(self.ui.persBaud.text())
		self.ui.persBaud.clear()

	def Connection(self):
		self.connStat = not self.connStat
		if self.connStat:
			port = str(self.ui.DeviceList.currentText())
			baud = self.ui.BaudList.currentText()
			self.device = serial.Serial(port,int(baud))
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%m:%S: connect to ")+ port +" "+baud)
			self.ui.ConnectionButton.setText("Disconnect")
		else:
			self.device.close()
			self.device=0
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%m:%S: disconnected"))
			self.ui.ConnectionButton.setText("Connect")

	def timerFunctions(self):
		self.time=time.strftime("%H:%m:%S")
		if self.device:
			data = comLib.readIncomeByte(self.device)
			if not isinstance(data, int):
				result=mvpl.decodeNMEA(data)
				self.ui.receivedText.appendPlainText(self.time+": "+str(result))
				self.graphicPlot()

	def graphicPlot(self):
		self.fig_Inlet.clf()
		ax1f1 = self.fig_Inlet.add_subplot(111)
		ax1f1.plot(np.random.rand(5),np.random.rand(5))
		self.canvasInlet.draw()
		
		

app = QtGui.QApplication(sys.argv)
window=MainWindow()
sys.exit(app.exec_())

