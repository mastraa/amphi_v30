#!usr/bin/python

import sys, serial
from PyQt4 import QtCore, QtGui, uic
import time

sys.path.append('libreria')

import comLib

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

		self.guiSetting()
		self.buttonFunction()

		self.ui.show()


	def guiSetting(self):
		self.ui=uic.loadUi(gui)#load gui
		self.ui.BaudList.addItems(baudValues)
		self.ui.connectionInfo.setReadOnly(1) #it will be scrollable

	def buttonFunction(self):
		self.ui.DeviceButton.clicked.connect(self.SerialCheck)
		self.ui.addValueButton.clicked.connect(self.addBaud)
		self.ui.ConnectionButton.clicked.connect(self.Connection)

	def SerialCheck(self):
		self.ui.DeviceList.clear()
		self.ui.DeviceList.addItems(comLib.checkSerialDevice()[1:])#first one is bluetooth device

	def addBaud(self):
		self.ui.BaudList.addItem(self.ui.persBaud.text())
		self.ui.persBaud.clear()

	def Connection(self):
		self.connStat = not self.connStat
		if self.connStat:
			port = str(self.ui.DeviceList.currentText())
			baud = self.ui.BaudList.currentText()
			self.device = serial.Serial(port,int(baud))
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%m:%S: connection to ")+ port +" "+baud)
			self.ui.ConnectionButton.setText("Disconnect")
		else:
			self.close()
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%m:%S: disconnected"))
			self.ui.ConnectionButton.setText("Connect")

app = QtGui.QApplication(sys.argv)
window=MainWindow()
sys.exit(app.exec_())

