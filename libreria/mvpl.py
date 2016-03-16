"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib, struct, time, csv
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np
from PyQt4 import QtGui

NMEA={};
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=[['b','l','f','f','f','f','f'],[]]#MVIC
NMEA[7]=[['b','l','l','L','L','L','f','f','f','f','f','f','f','b','b','b'],['tipo','lat','lon','gradi','date','times','vel','roll','pitch','yaw','temp','left','right','wspeed','wdir_1','wdir_2']]#MVUP
NMEA[8]=[['b','l','l','L','L','L','f','f','f','f'],[]]#MVUPC

def decodeNMEA(data):
	val=[]
	byteT=data[0]
	n=0
	for i in NMEA[byteT][0]:
		if i =='b':
			l=1
			val.append(data[n])
		else:
			if i=='i':
				l=2
			else:
				l=4
			array=data[n:n+l]
			while l<4:
				array.append(0)
				l=l+1
			array.reverse()
			val.append(comLib.byteToData(i, array))
			val[-1]=val[-1][0]
			if i == 'f':
				val[-1]=float("%.3f"%val[-1])
		n=n+l
	return val

def createDataStorage(tipo):#create index of data storage dictionary
	data={}
	for i in NMEA[tipo][1]:
		data[i]=[]
	data['tipo']=tipo
	return data

def storeData(buff, result):#for every iteration store last income data string in the dict
	i=1
	tipo=result[0]
	while i < len(NMEA[tipo][1]):
		if NMEA[tipo][1][i]=='times':
			buff[NMEA[tipo][1][i]].append(result[i]/1000)
		else:
			buff[NMEA[tipo][1][i]].append(result[i])
		i=i+1

def plot(data, figure):
	if data['tipo']==7:
		figura=figure['telemetria'][0]
		canvas=figure['telemetria'][1]
		roll, pitch, yaw, time, gradi=data['roll'],data['pitch'],data['yaw'],data['times'], data['gradi']
		scarroccio=[]
		for i in range(len(yaw)):
			scarroccio.append(gradi[i]-yaw[i])
		figura.clf()

		plot_1=figura.add_subplot(211)
		plot_1.plot(time[-25:],roll[-25:], label="roll")
		plot_1.plot(time[-25:],pitch[-25:], label="pitch")
		plot_1.plot(time[-25:],yaw[-25:], label="yaw")
		plot_1.legend(loc="upper right")
		plot_1.grid()

		plot_2=figura.add_subplot(212)
		plot_2.plot(time[-25:], scarroccio[-25:], label="scarr")
		plot_2.legend(loc="upper right")
		plot_2.set_xlabel('time[s]')
		plot_2.grid()


		canvas.draw()

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

def windView(monitor):
	monitor[1].display(12.3)

	

