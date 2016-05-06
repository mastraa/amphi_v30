"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib, struct, time, csv
import numpy as np
from PyQt4 import QtGui, QtCore

NMEA={}
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=[['b','l','f','f','f','f','f'],[]]#MVIC
NMEA[7]=[['b','l','l','L','L','L','f','f','f','f','f','f','f','b','b','b'],['tipo','lat','lon','gradi','date','times','vel','roll','pitch','yaw','temp','left','right','wspeed','wdir_1','wdir_2']]#MVUP
NMEA[8]=[['b','l','l','L','L','L','f','f','f','f'],[]]#MVUPC

fileNMEA={}
fileNMEA['$MVUP']=['time','lat','lon','vel','course','roll','pitch','yaw','ws','wd_1','wd_2','ld','ls']#it has other parameters that we don't use now


def decodeNMEA(data,NMEAType):#decodification of nmea data
	"""
	decoding simil NMEA byte string parsing byte to byte/int/float/long values
	data: byte string
	NMEAType: list of possible byte string
	return decoded data list
	"""
	val=[]
	tipo=data[0]#detecting type of string from the first byte received
	n=0
	for i in NMEAType[tipo][0]:#dataType list
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
	"""
	Create a dict with the the data names as labels
	tipo: byte_type, first byte received
	return the dict
	"""
	data={}#create dict
	for i in NMEA[tipo][1][1:]:#label for data incoming
		data[i]=[]#append new list in the dict with the label name
	data['tipo']=tipo#set tipo variable, it will be stored only one times
	return data

def storeData(buff, data, NMEAType):#for every iteration store last income data string in the dict
	"""
	Store data received in the dictionary
	buff: dictionary
	data: incoming data
	NMEAType: list of possible byte string
	"""
	i=1
	tipo=data[0]#search nmea type
	while i < len(NMEAType[tipo][1]):
		if NMEAType[tipo][1][i]=='times':
			buff[NMEAType[tipo][1][i]].append(data[i]/1000)
		else:
			buff[NMEAType[tipo][1][i]].append(data[i])
		i=i+1

def plot(data, extraData, figure, monitor, n):
	"""
	Plot graph
	data: dictionary with all data stored
	extraData: disctionary with some data created in post proc
	figure & monitor: space to plot
	n: number of data to plot

	this function must be review!!!
	"""
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

def Save(filename, data, NMEAType):
	"""
	Save dict data in text file
	"""
	file = open(filename, 'wb')
	head=NMEAType[data['tipo']][1]#list of labels
	for item in head:
		file.write(item+',')
	file.write('\n')
	for i in range(len(data['times'])):
		for item in head:
			if item=='tipo':#type byte is stored only one times
				file.write(str(data[item]))
			else:#other datas are stored in lists
				file.write(str(data[item][i]))
			file.write(',')#data separeted by comma
		file.write('\n')#new line
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

def readDataFile(file,fileType=None):
    """
    read data from simil NMEA Metis Vela code
    file: path to file, including extension
    fileType: NMEA ascii string list
    """
	if fileType is None:
		fileType = fileNMEA
    in_file = open(file,"r")
    content = in_file.readlines()
    in_file.close()
    nome,data,ora = content[0].split(' - ')
    time=[int(ora[4:6]),int(ora[2:4]),int(ora[0:2])+2]
    tipo=content[1].split(',')[0]
    data={
    label:[] for label in fileType[tipo]
    }
    temp=[]#temporary label store to recovery label of values knowing only his position (dict non preserve order)
    for label in fileType[tipo]:
    	temp.append(label)
    for item in content[1:]:
        values=item.split(',')
        a=0
        for i in range(1,len(values)):
        	try:
        		data[temp[a]].append(int(values[i]))#try to save as a int
        		print temp[a], values[i]
        		a=a+1
        		#ValueError occur when data from text is a label or when it is a floating point number
        		#Index error occur when label is written in the last position (label list of amphi is shorter)
        	except (ValueError, IndexError):
        		try:
        			data[temp[a]].append(float(values[i]))#try to save as a float
        			a=a+1
        		except (ValueError,IndexError):
        			pass

    return time,data
