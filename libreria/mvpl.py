"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib, struct, time, csv
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np
from PyQt4 import QtGui, QtCore

NMEA={};
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=[['b','l','f','f','f','f','f'],[]]#MVIC
NMEA[7]=[['b','l','l','L','L','L','f','f','f','f','f','f','f','b','b','b'],['tipo','lat','lon','gradi','date','times','vel','roll','pitch','yaw','temp','left','right','wspeed','wdir_1','wdir_2']]#MVUP
NMEA[8]=[['b','l','l','L','L','L','f','f','f','f'],[]]#MVUPC

def decodeNMEA(data):#decodification of nmea data
	val=[]
	tipo=data[0]
	n=0
	for i in NMEA[tipo][0]:#list of data type for the nmea tipo
		if i =='b':#byte
			l=1#leght = 1
			val.append(data[n])
		else:
			if i=='i':#integer
				l=2
			else:#float or long
				l=4
			array=data[n:n+l]#store bytes belong to the data
			while l<4:#in python integer has 4 bytes, in arduino_wiring two, so we need to increment the buffer
				array.append(0)
				l=l+1
			array.reverse()#we need the opposite order
			val.append(comLib.byteToData(i, array))#recompose value
			val[-1]=val[-1][0]
			if i == 'f':
				val[-1]=float("%.3f"%val[-1])
		n=n+l
	return val

def createDataStorage(tipo):#create index of data storage dictionary
	data={}#create dict
	for i in NMEA[tipo][1][1:]:#label for data incoming
		data[i]=[]#append new list in the dict with the label name
	data['tipo']=tipo#set tipo variable
	return data

def storeData(buff, data):#for every iteration store last income data string in the dict
	i=1
	tipo=data[0]#search nmea type
	while i < len(NMEA[tipo][1]):
		if NMEA[tipo][1][i]=='times':
			buff[NMEA[tipo][1][i]].append(data[i]/1000)
		else:
			buff[NMEA[tipo][1][i]].append(data[i])
		i=i+1

def plot(data, extraData, figure, monitor, n):
	if data['tipo']==7:
		figura=figure['telemetria'][0]
		canvas=figure['telemetria'][1]
		roll, pitch, yaw, time, gradi=data['roll'],data['pitch'],data['yaw'],data['times'], data['gradi']
		if yaw[-1]<0:
			rot=-yaw[-1]
		else:
			rot=360-yaw[-1]
		try:
			extraData['scarroccio'].append(abs(gradi[-1]-rot))
		except KeyError:
			extraData['scarroccio']=[]
			extraData['scarroccio'].append(abs(gradi[-1]-rot))
		figura.clf()

		plot_1=figura.add_subplot(311)
		plot_1.plot(time[-n:],roll[-n:], label="roll")
		plot_1.plot(time[-n:],pitch[-n:], label="pitch")
		plot_1.legend(loc="upper left")
		plot_1.grid()

		plot_2=figura.add_subplot(312)
		plot_2.plot(time[-n:],yaw[-n:], label="yaw")
		plot_2.plot(time[-n:], gradi[-n:], label="course")
		plot_2.legend(loc="upper left")
		plot_2.grid()

		plot_3=figura.add_subplot(313)
		plot_3.plot(time[-n:], extraData['scarroccio'][-n:], label="scarr")
		plot_3.legend(loc="upper left")
		plot_3.set_xlabel('time[s]')
		plot_3.grid()

		canvas.draw()

		monitor[0].display(data['roll'][-1])
		monitor[1].display(data['pitch'][-1])
		monitor[2].display(data['yaw'][-1])
		monitor[3].display(extraData['scarroccio'][-1])

def Save(filename, data):
	file = open(filename, 'wb')
	head=NMEA[data['tipo']][1]
	for item in head:
		file.write(item+',')
	file.write('\n')
	for i in range(len(data['times'])):
		for item in head:
			if item=='tipo':
				file.write(str(data[item]))
			else:
				file.write(str(data[item][i]))
			file.write(',')
		file.write('\n')
	file.close()

def windView(monitor, path, data):
	background = QtGui.QPixmap(path+'segna.jpg')
	item=monitor[0].addPixmap(background)
	monitor[1].fitInView(item)
	x_0,y_0=147,150
	l=100
	x=x_0+l*np.sin(data['wdir_1'][-1]*np.pi/180)
	y=y_0-l*np.cos(data['wdir_1'][-1]*np.pi/180)
	#monitor[0].removeItem(monitor[4])
	line = QtGui.QGraphicsLineItem(x_0,y_0,x,y)
	line.setPen(QtGui.QPen(QtCore.Qt.red, 5, QtCore.Qt.SolidLine))
	monitor[0].addItem(line)
	monitor[1].show()
	monitor[2].display(data['wdir_1'][-1])
	monitor[3].display(data['wspeed'][-1])

	

