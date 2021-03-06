#!usr/bin/python

# cd desktop/andrea/programmazione/programmi/python/amphi_v30
# cd Desktop/1001Vela/6000/Emessi/6024_ProgrammiDecodifica/amphi_v30
# cd C:\Users\SuperUser\Desktop\Programmazione\Sorgenti\amphi_v30


import sys, serial, time, struct, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.phonon import Phonon

import matplotlib
matplotlib.use("QT4Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvas
import numpy as np
import pyqtgraph as pg

def pathDefine(i):
	"""
	It defines path alternately for executable file or .py file
	"""
	if i == 0:
		path =  os.path.join(os.path.dirname(sys.executable), 'gui')
		sys.path.append(os.path.join(os.path.dirname(sys.executable),'libreria'))
	else:
		path="gui"
		sys.path.append('libreria')
	return path

guiPath=pathDefine(1) #1:terminal 0:exe

import comLib, mvpl, guiLib
from myPlotWidget import myPlotWidget, rollCurve, customCurve, plotDirector, Curve

#global definition
gui = "/MainGui.ui"
baudValues=["9600","57600","115200"]
path = os.path.dirname(os.path.realpath(__file__))

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		#variables
		global baudList, gui, path, guiPath
		self.connStat = 0 #connection status (not check data income, only connection activation)
		self.dataStatus = 0 #data income status
		self.device = 0 #device to connect
		self.interval=300 #millis
		self.i = 0 #frequenzimetro
		self.time=time.strftime("%H:%m:%S")
		self.timer=QtCore.QTimer(self)
		self.timer.timeout.connect(self.timerFunctions)
		self.timer.start(self.interval)
		self.data = self.extraData={}#data storage dict, extraData will take postProc data from some functions like scarroccio from mvpl.plot()
		self.lost=0 #lost data counter
		self.connTime= self.lastPackTime = 0
		self.icons={'status':['/img/redLed.png', '/img/greenLed.png', '/img/whiteLed.png']} #set path to led color

		self.media=Phonon.MediaObject(self)
		self.media.setTickInterval(250) #set tick video interval
		self.video=Phonon.VideoWidget(self)
		Phonon.createPath(self.media,self.video)

		# Create the various plots
		self.plotLabels = ['roll','pitch','yaw']
		self.curves = { s_label: Curve(label=s_label) for s_label in self.plotLabels}
		self.plotWidgets = { s_label: myPlotWidget(label='s_label') for s_label in self.plotLabels}
		# The director takes care of linking everything among themselves
		self.director = plotDirector(labels = self.plotLabels, curves=self.curves, plotWidgets=self.plotWidgets)

		self.figureSet() #setting figures for plotting
		self.guiSetting() #extra gui setting
		self.functionConnect() #connection between object and handlers

		self.ui.show() #show gui

	def figureSet(self):
		self.infFig=Figure()
		self.infCanv=FigureCanvas(self.infFig)

		self.telFig=Figure()
		self.telCanv=FigureCanvas(self.telFig)

		self.grafici={'infusione':[self.infFig,self.infCanv], 'telemetria':[self.telFig,self.telCanv]}

	def guiSetting(self):
		self.ui=uic.loadUi(guiPath+gui)#load gui
		self.ui.BaudList.addItems(baudValues)
		self.ui.connectionInfo.setReadOnly(1) #it will be scrollable
		self.ui.lcdTime.setDigitCount(8) #set time lcd digit
		self.ui.lcdTime.display(time.strftime("%H"+":"+"%M"+":"+"%S"))
		#plot set
		self.ui.infusionPlot.addWidget(self.infCanv)

		"""
		TODO: substitute telPlot list with a generic realTime list to use with all real time income data
		"""


		#set video analysis
		self.video.setMinimumSize(400,400)
		self.ui.videoLayout.addWidget(self.video)
		#set the wind_dir section
		self.wind=[] #list with all gui object for wind section
		self.wind.append(QtGui.QGraphicsScene(self))
		self.wind.append(self.ui.windDirView)
		self.wind.append(self.ui.windSpeed)
		self.wind.append(self.ui.windDir)
		self.wind.append(QtGui.QGraphicsLineItem(105,90,105,30)) #banderuola
		self.wind[4].setPen(QtGui.QPen(QtCore.Qt.red, 5, QtCore.Qt.SolidLine)) #arrow for banderuola
		self.wind[0].addItem(self.wind[4]) #add drawing to the scene
		self.ui.windDirView.setScene(self.wind[0])
		self.ui.windDirView.show()
		#set heading lcd section
		self.heading=[self.ui.rollLCD, self.ui.pitchLCD, self.ui.yawLCD, self.ui.scarLCD]
		#init led status
		guiLib.ImageToLabel(self.ui.connStatus, guiPath+self.icons['status'][2])

		#Data Analysis plot
		self.director.connectPlot(self.ui.plotVideoLayout)

	def functionConnect(self):
		"""
		Connect object to relative function
		"""
		self.ui.deviceCheckBtn.clicked.connect(self.SerialCheck)
		self.ui.addValueButton.clicked.connect(self.addBaud)
		self.ui.ConnectionButton.clicked.connect(self.Connection)
		self.media.stateChanged.connect(self.handleStateChanged)

		# Let the director handle the signals for the plotWidgets
		self.media.tick.connect(self.director.tickHandler)
		self.media.totalTimeChanged.connect(self.director.totalTimeChangedHandler)

		# Connect TimeSincTxt and TimeSetOK to the director
		self.ui.TimeSincTxt.textChanged.connect(self.director.syncTextChangedHandler)
		self.ui.TimeSincTxt.textEdited.connect(self.director.syncTextChangedHandler)
		self.ui.TimeSincTxt.returnPressed.connect(self.director.syncTextConfirmHandler)
		self.ui.TimeSetOK.clicked.connect(self.director.syncTextConfirmHandler)

		# Add the button to the director
		self.director.button = self.ui.TimeSetOK

		self.ui.loadVideo.clicked.connect(self.handleButton)
		self.ui.playVideo.clicked.connect(lambda:self.playVideo(1))
		self.ui.stopVideo.clicked.connect(lambda:self.playVideo(2))
		self.ui.pauseVideo.clicked.connect(lambda:self.playVideo(0))

		# Connect the data file loading
		self.ui.LoadDataTxt.clicked.connect(self.director.loadDataFile)

	def SerialCheck(self):
		"""
		Check if any device is connected to serial port
		if there is any add it drop down menu
		"""
		self.ui.DeviceList.clear()
		self.ui.DeviceList.addItems(comLib.checkSerialDevice())

	def addBaud(self):
		"""
		Add new badRate to the list and clear text box
		"""
		self.ui.BaudList.addItem(self.ui.persBaud.text())
		self.ui.persBaud.clear()

	def Connection(self):
		"""
		Connection to device
		"""
		self.connStat = not self.connStat #switch connection status 1:connect, 0:disconnect
		self.dataStatus = 1 #reset data status flag
		if self.connStat:
			port = str(self.ui.DeviceList.currentText())
			baud = self.ui.BaudList.currentText()
			self.device = serial.Serial(port,int(baud))
			self.connTime = self.lastPackTime = time.time() #reset timers
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%M:%S: connect to ")+ port +" "+baud) #display connection parameters on monitor
			self.ui.ConnectionButton.setText("Disconnect") #change button text
			guiLib.ImageToLabel(self.ui.connStatus, guiPath+self.icons['status'][1]) #set led connection color
		else:
			self.device.close()
			self.device = self.lost = self.connTime=0 #reset variables
			self.ui.connectionInfo.appendPlainText(time.strftime("%d/%m/%y %H:%M:%S: disconnected")) #display connection parameters on monitor
			self.ui.ConnectionButton.setText("Connect") #change button text
			self.infoSave()
			self.data.clear() #clear store data dict
			self.extraData.clear()

	def timerFunctions(self):
		self.time=time.strftime("%H:%M:%S")
		self.i +=1 #cycle counter increment (for 1hz activation)
		if self.i >= 1000/self.interval: #activation at one hertz
			self.i = 0 #reset counter
			self.oneHertz(self.time)
		if self.device: #if any device is connected
			income = comLib.readIncomeByte(self.device)#read byte on serial buffer
			if isinstance(income, int):#list:ok, int: error
				if income==2:#no starter error
					comLib.readUntil(self.device,'*')#empty serial income buffer until last known character
					self.lost=self.lost+1#increment losts packet counter
					self.ui.lostPackLCD.display(self.lost)#show lost Pack quantity from connection
			else:#no error
				self.lastPackTime=time.time()#update last package time
				result=mvpl.decodeNMEA(income,mvpl.NMEA)#decode data
				self.ui.receivedText.appendPlainText(self.time+": "+str(result[0]))
				if len(self.data)==0:#if it is first data arrived
					self.data=mvpl.createDataStorage(result[0])#create data storage, giving type byte
					self.createPlotWidget()
				if self.dataStatus == 0: #if dataStatus is setted false...
					self.dataStatus = 1 #...reset it...
					guiLib.ImageToLabel(self.ui.connStatus, guiPath+self.icons['status'][1])#...and change led status color
				mvpl.storeData(self.data, result, mvpl.NMEA)
				self.realTimeView()#show data in telemetry section


	def oneHertz(self, time): #activate at one hertz
		self.ui.lcdTime.display(time)# print time on digital clock
		self.infoConn()

	def infoConn(self):#check connection status and alert user
		if self.connTime:
			now=time.time()
			self.ui.connTimeLCD.display(int(now-self.connTime))#print connection time
			if (now-self.lastPackTime>5): #if more than x seconds from last received data are passed...
				self.dataStatus = 0 #set status to false
				guiLib.ImageToLabel(self.ui.connStatus, guiPath+self.icons['status'][0]) #change status led to red

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
				mvpl.Save(fileName, self.data, mvpl.NMEA)

	def createPlotWidget(self):
		"""
		create PlotWidget list for real time data
		set for the widget the correct label
		set the widget in the correct QLayout

		TODO: now it has only implementation for telemetry view, extend to other incoming data type
		"""
		self.realTimePlot=[]
		self.realTimePlot.append(myPlotWidget(tipology='static'))
		self.realTimePlot.append(myPlotWidget(tipology='static'))

		if self.data['tipo']==7:
			self.realTimePlot[0].labelMod(['roll','pitch'])
			self.realTimePlot[1].labelMod(['scarroccio','gradi'])
			for item in self.realTimePlot:
				self.ui.telPlotLayout.addWidget(item)

	def realTimeView(self):
		mvpl.postProcData(self.data)
		monitor=[]
		monitor.extend(self.wind)
		monitor.extend(self.heading)
		mvpl.cockpitView(monitor, guiPath+'/img/', self.data)
		for item in self.realTimePlot:
			item.staticPlot(self.data)

	def handleStateChanged(self):
		pass

	def playVideo(self, state):
		"""
		play/pause/stop the video
		1: play, 2:stop, 0:pause
		"""
		if state == 0:
			self.media.pause()
		elif state == 1:
			self.media.play()
		else:
			self.media.stop()

	def handleButton(self):
		if self.media.state()==Phonon.PlayingState:
			self.media.stop()
		else:
			path=QtGui.QFileDialog.getOpenFileName(self,self.ui.loadVideo.text())
			if path:
				self.media.setCurrentSource(Phonon.MediaSource(path))



app =QtGui.QApplication(sys.argv)
window=MainWindow()
sys.exit(app.exec_())
