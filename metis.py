#!usr/bin/python

# cd desktop/andrea/programmazione/programmi/python/amphi_v30
# cd Desktop/1001Vela/6000/Emessi/6024_ProgrammiDecodifica/amphi_v30
# cd C:\Users\SuperUser\Desktop\Programmazione\Sorgenti\amphi_v30


import sys, serial, time, struct, os
from PyQt4 import QtCore, QtGui, uic

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np

sys.path.append('libreria')

import comLib, mvpl

#global definition
gui = "gui/MainGui.ui"
#saveDialogGui="gui/saveDialog.ui"
saveDialogGui="gui/widget.ui"
baudValues=["9600","57600","115200"]
path = os.path.dirname(os.path.realpath(__file__))

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		#variables
		global baudList, gui, path
		self.connStat = 0
		self.device = 0 #device to connect
		self.interval=300 #millis
		self.time=time.strftime("%H:%m:%S")
		self.timer=QtCore.QTimer(self)
		self.timer.timeout.connect(self.timerFunctions)
		self.timer.start(self.interval)
		self.data={}#data storage dict

		self.figureSet()
		self.guiSetting()
		self.buttonFunction()

		self.ui.show()

	def figureSet(self):
		self.infFig=Figure()
		self.infCanv=FigureCanvas(self.infFig)

		self.telFig=Figure()
		self.telCanv=FigureCanvas(self.telFig)

		self.grafici={'infusione':[self.infFig,self.infCanv], 'telemetria':[self.telFig,self.telCanv]}

	def guiSetting(self):
		self.ui=uic.loadUi(gui)#load gui
		self.ui.BaudList.addItems(baudValues)
		self.ui.connectionInfo.setReadOnly(1) #it will be scrollable
		self.ui.infusionPlot.addWidget(self.infCanv)
		self.ui.telPlot.addWidget(self.telCanv)

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
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%M:%S: connect to ")+ port +" "+baud)
			self.ui.ConnectionButton.setText("Disconnect")
		else:
			self.device.close()
			self.device=0
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%M:%S: disconnected"))
			self.ui.ConnectionButton.setText("Connect")
			self.infoSave()
			self.data.clear()#clear store data dict

	def timerFunctions(self):
		self.time=time.strftime("%H:%M:%S")
		if self.device:
			income = comLib.readIncomeByte(self.device)
			if not isinstance(income, int):
				result=mvpl.decodeNMEA(income)
				self.ui.receivedText.appendPlainText(self.time+": "+str(result[0]))
				if len(self.data)==0:
					self.data=mvpl.createDataStorage(result[0])
				mvpl.storeData(self.data, result)
				mvpl.plot(self.data, self.grafici)

	def infoSave(self):
		info=QtGui.QMessageBox()
		info.setIcon(QtGui.QMessageBox.Information)
		info.setText("Disconnecting you will lose all data, do you want to save?")
		info.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
		info.buttonClicked.connect(self.saveData)
		info.exec_()

	def saveData(self, i):
		if i.text()=="OK":
			pathFile=path+"/fileStore/"+time.strftime("%y%m%d%H%M")+".csv"
			fileName=QtGui.QFileDialog.getSaveFileName(self, 'Save Data', pathFile, selectedFilter='*.csv')
			if fileName:
				mvpl.Save(fileName, self.data)

app = QtGui.QApplication(sys.argv)
window=MainWindow()
sys.exit(app.exec_())

